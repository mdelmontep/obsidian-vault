---
title: integraciones bancarias facturaia — psd2 + csv/n43 + pasarelas
date: 2026-05-11
source: claude-code-session
tags: [facturaia, open-banking, psd2, conciliacion, spec]
---

# Integraciones bancarias para FacturaIA

Cómo llevar la conciliación bancaria de "movimientos vacíos" (estado actual) a "facturas pagadas/cobradas automáticamente sin intervención del usuario".

## Estado actual del repo (qué NO falta)

- Tabla `movimientos_bancarios` (migration 043) genérica: `org_id, fecha, importe, descripcion, referencia, cuenta, fuente, created_at`. RLS por `org_members`. Cualquier origen escribe ahí.
- Triggers BD `auto_mark_pagada_on_bank_match` y `auto_mark_pagadas_on_movimiento` (migration 061) — casan factura recibida ↔ movimiento bidireccionalmente, respetan `tolerancia_euros` (10€), `ventana_dias` (±30d), `auto_marcar_cobradas` desde `org_module_config`. Cubren todos los flujos (n8n OCR, manual, API v1, voz) sin tocar código TS por caller.
- Módulo "Conciliación bancaria" (`catalog.ts:122`, plan Pro add-on 19€) con config schema editable.
- Cross-check OCR `bankMatchCheck` (`src/lib/ocr/anomaly.ts:192`) levanta anomalía `no_bank_match` si entran movimientos pero ninguno cuadra con el total extraído.
- Métricas vivas en `/api/modules/conciliacion/metrics` (count `factura_pagada_auto` 30d).

## Lo que SÍ falta (gap)

- **Cero ingesta**: la tabla está vacía en todas las orgs salvo seeds de test. Ningún endpoint ni UI permite escribir movimientos hoy.
- Sin conexión PSD2 ni agregador.
- Solo cubre recibidas → `pagada`. Las emitidas → `cobrada` no tienen trigger simétrico (revisable, sería análogo con signo positivo y `fecha_cobro` de migration 034).
- Match 1:1 por importe ± tolerancia. No agrupa cobros fraccionados ni separa transferencias agregadas.
- Sin job de reconciliación masiva (solo en el momento del INSERT/UPDATE).

## Tres opciones de ingesta — comparativa

### Opción A — Agregador PSD2 (recomendado a medio plazo)

FacturaIA no es TPP autorizado por Banco de España. Usa un agregador que sí lo es y te expone REST sobre 2.000+ bancos europeos.

| Proveedor | Pros | Contras |
|---|---|---|
| **GoCardless Bank Account Data** (ex-Nordigen) | Tier gratuito real, cobertura ES amplia, docs simples, sandbox limpio | Refresco cada 4h (no real-time), consent 90-180d con renovación |
| **Tink (Visa)** | Real-time webhooks, categorización propia, soporte serio | Caro (~500€/mes suelo), contrato comercial |
| **TrueLayer** | Buena DX, EU cobertura, datos enriquecidos | Pricing por API call, sin tier gratis útil |
| **Salt Edge / Fintecture / Belvo** | Alternativas | Cobertura ES menor que GoCardless |

**Recomendación**: empezar con **GoCardless BAD**. Cubre conciliación (no necesitamos real-time para casar facturas) con coste 0 hasta volumen serio.

**Flujo PSD2 estándar (igual en todos):**

```
1. Usuario en /settings/conciliacion → "Conectar banco"
2. POST a tu backend → creas requisition / link en el agregador
3. Redirect a URL del agregador → user se loguea en su banco (SCA)
4. Banco redirige a tu callback con consent_id
5. Guardas (org_id, bank_id, consent_id_cifrado, accounts[], expires_at) en BD
6. Cron N veces/día: por cada consent activo, GET /accounts/{id}/transactions
   → upsert a movimientos_bancarios con fuente='psd2_gocardless'
7. Antes de expirar (90-180d), recordatorio al user para renovar consent
```

**Qué hay que construir en el repo:**

- Migración `bank_consents` (org_id, provider, consent_id_cifrado AES-256-GCM con `CREDENTIAL_ENCRYPTION_KEY`, accounts jsonb, status, expires_at, last_synced_at, last_sync_error). RLS por org_members.
- `POST /api/integrations/bank/connect` → crea requisition, devuelve URL auth.
- `GET /api/integrations/bank/callback` → recibe consent_id, persiste, lista cuentas.
- `POST /api/internal/bank-sync` (x-service-key) → cron Dokploy 4-6h: itera consents activos, fetch transactions, upsert con dedupe.
- Dedupe idempotente: clave única `(org_id, provider_transaction_id)` o fallback `hash(fecha, importe, descripcion, referencia)` si el provider no da ID estable.
- UI tab "Bancos" en `/settings/conciliacion`: estado por consent (verde/ámbar/rojo según `last_sync_error` + `expires_at`), última sync, cuentas, botón renovar.
- Notif `bank_consent_expiring` 7d antes de expirar → campanita.

Estimación: 1-2 semanas con sandbox + 1 banco real (BBVA o Santander), después añadir bancos es config.

### Opción B — Import de archivo (puente cero-fricción, recomendado HOY)

Antes de PSD2: **Norma 43** (formato AEB español que todos los bancos exportan). Sin auth, sin agregador, sin coste recurrente.

**Qué hay que construir:**

- UI en `/settings/conciliacion` (o tab dentro del modal del módulo): drag&drop archivo.
- Parser Norma 43 (formato fijo posicional AEB-43, doc pública). Alternativa o complemento: parsers por banco específico (BBVA/Santander/CaixaBank/Sabadell tienen CSVs distintos) — más frágiles, no recomendable como primer paso.
- Preview de mapping (fecha · importe · concepto · ref) antes de insertar.
- INSERT batch a `movimientos_bancarios` con `fuente='n43'` o `csv_<banco>'`.
- Dedupe por hash `(fecha, importe, descripcion, referencia)` para reimports.
- Mostrar resumen post-import: "N movimientos importados, M duplicados ignorados, X facturas marcadas como pagadas automáticamente" (este último viene del trigger 061 sin esfuerzo extra).

Estimación: **1-2 días**. Desbloquea conciliación para cualquier cliente con un banco español. Es lo que el 90% de gestorías hace hoy a mano.

### Opción C — Pasarelas de cobro (Stripe, GoCardless Direct Debit, Redsys)

No es banco, es el otro flujo de dinero. Si el cliente cobra con Stripe Invoice o Redsys, sus webhooks ya son conciliación directa:

```
Webhook Stripe invoice.paid →
  match por metadata.factura_id (lo seteas al crear el cobro) →
  UPDATE facturas SET estado='cobrada', fecha_cobro=event.created
```

Sin pasar por extracto bancario. **Módulo separado** ("pasarelas de cobro"), no parte de conciliación. Pero mata dos pájaros: si Stripe dice "ha pagado", no esperas al movimiento.

## Roadmap recomendado

1. **Norma 43 import** (1-2 días) — desbloquea YA. Compatible con triggers existentes, sin coste recurrente. Empezar aquí.
2. **Trigger simétrico emitidas → cobrada** (~horas) — copia de 061 con `tipo='emitida'`, signo positivo, `fecha_cobro` desde migration 034.
3. **Vista de huérfanos en `/settings/conciliacion`** (~1 día) — dos listas: movimientos sin factura + facturas sin movimiento. Botón manual "linkar" para casos que el trigger no pilla (importes agrupados, fraccionados).
4. **GoCardless BAD PSD2** (1-2 semanas) — cuando el cliente se canse de subir N43 semanal. Reutiliza tabla y triggers tal cual.
5. **Tink/TrueLayer** sólo si llegan clientes que paguen por real-time o categorización propia.
6. **Pasarelas de cobro** (Stripe Invoice + Redsys) — módulo aparte. Cuando se cablee Stripe checkout para add-ons (NEXT del hub).

## Riesgos y decisiones pendientes

- **Almacenar consent_id PSD2** — cifrado obligatorio. Robar consent = leer extracto bancario del cliente. Usar `CREDENTIAL_ENCRYPTION_KEY` ya existente o key separada `BANK_CONSENT_ENCRYPTION_KEY` para rotación independiente.
- **Compliance** — GoCardless BAD es licencia PSD2 AIS suya, no necesitas pasporte. Pero el T&C de FacturaIA debe declarar el procesado de datos bancarios y el consentimiento. Revisar con Dani.
- **Match 1:1 limitación** — clientes con cobros fraccionados o transferencias agrupadas necesitarán manual override. Trigger 061 actual sólo pilla el caso simple. Para módulo "pro pro" → IA Claude para sugerir matches multi-line (queda en `LATER`).
- **Conciliación de facturas emitidas vs estado portal** — agency-portal puede mostrar `cobrada` de un sistema externo (Stripe). Coherencia trigger BD vs estado portal → ver regla "shadow doc" del CLAUDE.md.

## Decisiones cerradas en este análisis

- **Empezar por Norma 43, no por PSD2** — coste 0, valor 80%, mismo back-end. Decisión justificada por progresividad y por el hecho de que la tabla `movimientos_bancarios` ya está fuente-agnóstica.
- **GoCardless BAD como primer agregador**, no Tink ni Plaid — España + tier gratis + cobertura.
- **Pasarelas de cobro como módulo aparte**, no extensión de conciliación — flujos distintos, webhooks distintos, billing distinto.

## Referencias

- Norma AEB-43 (formato bancario español): https://www.aebanca.es/
- GoCardless Bank Account Data docs: https://bankaccountdata.gocardless.com/
- Trigger 061 (lógica de matching ya en prod): `supabase/migrations/061_conciliacion_auto_marcar_pagada.sql`
- Tabla movimientos: `supabase/migrations/043_movimientos_bancarios.sql`
- Spec antigua conciliación (referencia histórica): `facturaia/docs/superpowers/specs/2026-04-21-conciliacion-bancaria-design.md`
