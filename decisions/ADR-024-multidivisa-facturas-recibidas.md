---
title: "ADR-024: Multidivisa en facturas recibidas — extensión del modelo de mig 173"
date: 2026-05-29
status: propuesto
tags: [facturaia, multidivisa, recibidas, ocr, fiscal]
---

# ADR-024: Multidivisa facturas recibidas

## Contexto

La mig 173 (ADR-022) implementó multidivisa completo para **emitidas**: columnas generadas `base_eur`/`total_eur`, `resolveTipoCambio()` con BCE, `fx_rates` cache, 27 divisas ISO.

Las **recibidas** quedaron fuera: `bandeja_ingesta` no tiene campos de divisa, el OCR no extrae la moneda, y al aprobar una factura recibida siempre se crea con `moneda='EUR'`. Esto genera datos fiscales erróneos para proveedores como AWS, Stripe, Adobe, Notion que facturan en USD.

Impacto fiscal real:
- Modelo 303: IVA soportado calculado sobre EUR incorrecto
- Cashflow: gastos proyectados en EUR incorrecto
- Modelo 347: umbral €3.005,06 calculado sobre nominal, no EUR equivalente

## Decisión

Extender el mismo modelo de mig 173 a `bandeja_ingesta` y al flujo de aprobación de recibidas, con estas reglas:

1. **Tipo de cambio = BCE a fecha de devengo** (LIVA art 6.1.j). Editable por el usuario pero con warning si desviación >5% del BCE.
2. **OCR extrae `moneda` + `confianza_moneda`** ('alta'|'media'|'baja'). Baja confianza → `requires_human_review=true`.
3. **`manual_requerido`** como fuente cuando BCE no tiene cobertura (festivos). Bloquea aprobación hasta que el usuario indique tipo manualmente.
4. **Propagación atómica**: endpoint `POST /api/recibidas/[id]/aprobar` copia FX de bandeja → factura en transición `sin_aprobar → pendiente`.
5. **`facturas` sin nuevas columnas** — ya tiene todo desde mig 173.
6. **ISP diferido** — sprint separado.

## Alternativas rechazadas

- `tipo_cambio_correcciones JSONB` en `facturas` para audit trail: anti-patrón (CLAUDE.md §Integración crítica en JSONB). Usar `audit_log`.
- Bloquear la aprobación siempre que hay divisa extranjera: demasiada fricción. Solo bloquear si `manual_requerido`.
- Requerir siempre BCE (sin override): inválido legalmente en casos con cobertura de cambio contractual.

## Consecuencias

- **Mig 177** — 6 columnas en `bandeja_ingesta` (4 FX + 2 OCR confianza)
- **Nuevo endpoint** `POST /api/recibidas/[id]/aprobar`
- **Prompt OCR** actualizado para extraer moneda con confianza
- **UI**: drawer bandeja con confirmación FX, chip en tabla recibidas, warning desviación
- **Copiloto**: tool `revisarBandejaMoneda` con historial de proveedor
- **Notificaciones**: alerta cuando llega factura en divisa extranjera con impacto >5%

## Spec completa

[[facturaia-multidivisa-recibidas]]
