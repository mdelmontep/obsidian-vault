---
title: "Spec: Multidivisa Facturas Recibidas"
date: 2026-05-29
source: sesión análisis 4 agentes paralelos (BD/Backend · OCR/IA · UX/Frontend · Fiscal/Legal)
tags: [facturaia, multidivisa, recibidas, ocr, fiscal, sprint]
---

# Multidivisa — Facturas Recibidas

## Problema

Las facturas recibidas (email/WA → OCR → `bandeja_ingesta` → `facturas.tipo='recibida'`) se contabilizan siempre en EUR aunque el proveedor facture en USD/GBP/etc. Resultado: `base_eur`/`total_eur` erróneos → modelo 303, cashflow y modelo 347 con datos fiscales incorrectos.

Las facturas **emitidas** tienen multidivisa completo desde mig 173. Este sprint extiende ese modelo a recibidas.

## Normativa fiscal aplicable

- **LIVA art 6.1.j**: tipo de cambio = BCE a fecha de devengo (obligatorio, no negociable con el proveedor)
- Frankfurter (`api.frankfurter.dev`) sirve tipos BCE oficiales — implementación actual correcta ✅
- **VeriFACTU**: solo aplica a emitidas, NO a recibidas ✅
- **Modelo 347**: umbral €3.005,06 sobre EUR equivalente (`base_eur`), no sobre nominal divisa
- **Diferencias de cambio**: resultado financiero (IRPF/IS), NO IVA → no tocar 303
- **ISP (Inversión Sujeto Pasivo)**: pendiente sprint separado P2

## Decisiones de arquitectura

- `tipo_cambio` es editable por el usuario → warning no-bloqueante si desviación >5% del BCE
- Si BCE no tiene cobertura (festivo/fin de semana): `tipo_cambio_fuente='manual_requerido'` → bloquea aprobación hasta que usuario lo indique manualmente
- `tipo_cambio_correcciones JSONB` en `facturas` **rechazado** (anti-patrón CLAUDE.md) → usar `audit_log`
- `fx_rates` ya existe desde mig 173, no recrear

Ver [[ADR-024-multidivisa-facturas-recibidas]]

---

## Sprint 1 — BD + Backend core (~3h)

### Migración 177

```sql
-- 177_multidivisa_bandeja_ingesta.sql
ALTER TABLE bandeja_ingesta
  ADD COLUMN IF NOT EXISTS moneda TEXT NOT NULL DEFAULT 'EUR',
  ADD COLUMN IF NOT EXISTS tipo_cambio NUMERIC(18,8) NOT NULL DEFAULT 1,
  ADD COLUMN IF NOT EXISTS tipo_cambio_fuente TEXT,
  ADD COLUMN IF NOT EXISTS tipo_cambio_fecha DATE,
  ADD COLUMN IF NOT EXISTS confianza_moneda TEXT,
  ADD COLUMN IF NOT EXISTS notas_moneda TEXT;

ALTER TABLE bandeja_ingesta
  ADD CONSTRAINT bandeja_moneda_iso CHECK (moneda IN (
    'EUR','USD','GBP','CHF','JPY','CAD','AUD','NZD','SEK','NOK','DKK',
    'PLN','CZK','HUF','RON','BGN','MXN','BRL','CNY','HKD','SGD','INR',
    'ZAR','TRY','ILS','KRW','AED','MAD')),
  ADD CONSTRAINT bandeja_tipo_cambio_positivo CHECK (tipo_cambio > 0),
  ADD CONSTRAINT bandeja_tipo_cambio_fuente_valida CHECK (
    tipo_cambio_fuente IS NULL OR tipo_cambio_fuente IN (
      'bce','manual','bce_override','manual_requerido')),
  ADD CONSTRAINT bandeja_moneda_eur_tc1 CHECK (moneda <> 'EUR' OR tipo_cambio = 1),
  ADD CONSTRAINT bandeja_confianza_moneda_valida CHECK (
    confianza_moneda IS NULL OR confianza_moneda IN ('alta','media','baja'));
```

`facturas` — **sin cambios**. Ya tiene columnas generadas `base_eur`/`total_eur` desde mig 173.

### Archivos backend

| Archivo | Cambio |
|---|---|
| `src/app/api/internal/whatsapp/ocr-process/route.ts` | Tras extraer `moneda` del OCR, llamar `resolveTipoCambio()` y persistir en `bandeja_ingesta`. Si BCE falla → `tipo_cambio_fuente='manual_requerido'` + `aviso`. No bloquear flujo OCR. |
| `src/lib/email/process-attachments.ts` | Al crear `bandeja_ingesta` desde email: inicializar `moneda='EUR'`, `tipo_cambio=1` |
| `src/app/api/upload/route.ts` | Ídem |
| `src/app/api/internal/whatsapp/ingesta/route.ts` | Ídem |
| `src/app/api/recibidas/[id]/aprobar/route.ts` | **NUEVO** — `POST`. Transición `sin_aprobar→pendiente`. Copia moneda/tipo_cambio de bandeja→factura si factura aún tiene EUR. Rechaza 422 si `fuente='manual_requerido'`. Emite `audit_log accion='recibida_aprobada_fx'`. |
| `src/lib/types.ts` | Añadir `'manual_requerido'` a `TipoCambioFuente`. Añadir `confianza_moneda`/`notas_moneda` a `BandejaItem.datos_extraidos`. |

### Criterios de aceptación

- [ ] Factura email USD → bandeja tiene `moneda='USD'`, `tipo_cambio≈0.9259`, `fuente='bce'`
- [ ] Factura AED → `fuente='manual_requerido'`, `aviso` con instrucción
- [ ] `POST /api/recibidas/[id]/aprobar` con `manual_requerido` → 422 claro
- [ ] Factura aprobada → `facturas.moneda='USD'`, `base_eur`/`total_eur` calculados
- [ ] `audit_log` tiene entrada con moneda, tipo_cambio, fuente

---

## Sprint 2 — OCR extrae moneda (~2h)

### Cambio de prompt OCR

Añadir al bloque de extracción de `buildExtractionInstruction()`:

```
"moneda": "ISO 4217 (EUR, USD, GBP, CHF, BRL, etc.)",
"confianza_moneda": "alta|media|baja",
"notas_moneda": "razón: símbolo €, contexto UK, ambiguo $ sin país..."

REGLAS:
1. Símbolo € → EUR alta. £ → GBP alta. ¥ → JPY alta.
2. Símbolo $ + "USA/United States" → USD alta.
3. Símbolo $ + "Canada" → CAD alta.
4. Símbolo $ sin país → USD baja. Nota: "$ ambiguo sin contexto".
5. Símbolo $ + "Mexico/México" → MXN media.
6. Código ISO explícito → alta.
7. Sin símbolo → EUR media.
```

### Interface

```typescript
// OcrExtractedFields añadir:
confianza_moneda?: 'alta' | 'media' | 'baja'
notas_moneda?: string
```

### Anomalías

- Nueva anomalía `moneda_baja_confianza` (severity `medium`) cuando `confianza_moneda==='baja'`
- Fuerza `requires_human_review=true` en ese caso

### Casos reales esperados

| Proveedor | Extracción | Confianza |
|---|---|---|
| AWS | USD | alta |
| Stripe (empresa belga) | EUR | alta |
| Adobe (USA) | USD | alta |
| Notion | USD | alta |
| Proveedor MX con `$` | MXN | media |
| Factura sin símbolo | EUR | media |

### Criterios de aceptación

- [ ] Factura AWS → `moneda='USD'`, `confianza='alta'`, sin revisión
- [ ] Factura con `$` sin país → `confianza='baja'`, `requires_human_review=true`
- [ ] GBP correctamente detectado

---

## Sprint 3 — UX (~3h)

### Hallazgo clave

El editor inline de `/recibidas` **ya tiene** selector de moneda y tipo de cambio (líneas 1688-1719 `facturas-view.tsx`). La función `fetchFxRate()` ya existe. El 80% de la infraestructura frontend está lista.

### Cambios reales necesarios

**`details-panel.tsx` (drawer bandeja):**
- Si `datos_extraidos.moneda ≠ 'EUR'`: card "Moneda detectada: USD" con badge de confianza
- Si `confianza_moneda==='baja'`: badge ámbar "Verificar moneda"
- Si `tipo_cambio_fuente==='manual_requerido'`: bloque rojo con input y botón "Usar tipo BCE hoy"
- Mostrar equivalencia EUR en tiempo real: "1.000 USD = 925,90 €"

**Tabla `/recibidas`:**
- Chip `[USD]` junto al importe si `moneda ≠ 'EUR'`
- Icono alerta si `fuente==='manual_requerido'`

**Bulk approve:**
```typescript
if (facturas.some(f => f.tipo_cambio_fuente === 'manual_requerido')) {
  toast.error("Hay facturas con tipo de cambio pendiente de confirmar")
  return
}
```

**Warning desviación >5%:** no-bloqueante, texto "El tipo BCE del [fecha] es [valor]. ¿Tienes acuerdo contractual previo?"

**Nuevo componente** `DivisaBadge`: `src/components/ui/divisa-badge.tsx`
```tsx
// { moneda: string, size?: 'sm'|'md', confianza?: 'alta'|'media'|'baja' }
```

### Criterios de aceptación

- [ ] Drawer bandeja con USD muestra badge + equivalencia EUR
- [ ] `manual_requerido` → bloque rojo con input activo
- [ ] Chip `[USD]` en tabla recibidas
- [ ] Bulk approve con FX pendiente bloquea con toast
- [ ] Warning visual si tipo manual >5% BCE

---

## Sprint 4 — Copiloto + Notificaciones (~2h)

### Copiloto: tool `revisarBandejaMoneda`

- Input: `ingesta_id`, `org_id`
- Busca historial de facturas del proveedor → sugiere moneda más frecuente
- Respuesta: "Este proveedor facturó en USD en 5 ocasiones anteriores — ¿confirmo USD?"
- Ubicación: `src/lib/copiloto/tools/revisarBandejaMoneda.ts`

### Copiloto: hint automático

Cuando se abre con bandeja `requires_human_review=true` por moneda: propone directamente confirmación.

### Notificaciones

- Trigger: recibida con `moneda ≠ 'EUR'` entra a bandeja
- Severity `warning` si impacto FX >5%
- Severity `critical` si además `confianza='baja'`
- CTA: enlace a bandeja con id pre-abierto
- Badge sidebar: count de facturas FX pendientes

### Criterios de aceptación

- [ ] Copiloto sugiere moneda correcta para proveedor con historial
- [ ] Notificación aparece cuando llega factura USD con impacto >5%
- [ ] Badge sidebar actualizado en tiempo real

---

## Sprint P2 (futuro) — ISP

Detección automática de Inversión Sujeto Pasivo:
- OCR detecta `pais ∈ {US, GB, CA, AU...}` + concepto = servicio → sugerir ISP
- Checkbox en drawer "¿Inversión sujeto pasivo?"
- Casillas 303 correctas (12/13 devengado + 28/29 deducible → efecto neutro)
- Bloquear deducción IVA para terceros-país sin ISP activo

---

## Reglas fiscales hardcodeadas

| Regla | Estado |
|---|---|
| Tipo = BCE fecha devengo (LIVA art 6.1.j) | `resolveTipoCambio()` ✅ |
| Warning si >5% vs BCE | Sprint 3 |
| 303 suma `base_eur` en EUR | ✅ ya correcto |
| 347 umbral sobre EUR equivalente | ✅ ya usa `base_eur` |
| VeriFACTU solo emitidas | ✅ no toca recibidas |
| Diferencias de cambio NO van a 303 | Nota informativa en copiloto v2 |

---

## Orden de ejecución

```
Sprint 1 (BD+backend)  ─┬─  Sprint 2 (OCR)
     ~3h                │       ~2h
                        └→  Sprint 3 (UX)
                                ~3h
                                 └→  Sprint 4 (IA+notif)
                                          ~2h
                                    Total: ~10h
```

Sprints 1 y 2 pueden ejecutarse en paralelo (archivos disjoint).
Sprint 3 depende de Sprint 1. Sprint 4 depende de 2 y 3.
