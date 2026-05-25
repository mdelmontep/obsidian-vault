---
title: acciones de estado fiscal vs sombra en sistema externo
date: 2026-05-08
source: claude-code-session
tags: [fiscal, sombra, integracion, agency-portal, facturaia]
---

Si una entidad tiene `documento_sombra` emitido en sistema externo (TuFacturaIA, AEAT, Stripe Invoice, Verifactu, GoCardless), las acciones que cambian estado (marcar pagada, anular, reenviar) deben ir vía ese sistema, NO actualizar solo el local.

Caso real (agency-portal): `cancelInvoiceAction` marcaba `agency_invoices.status='cancelled'` mientras la factura seguía viva en TuFacturaIA → portal y AEAT desincronizados. Si Hacienda cruza datos, multa.

Patrón correcto en UI: cuando hay `shadow.remoteId`, renderizar la botonera del sistema externo (`<FacturaiaActions>`) y ocultar las acciones locales de cambio de estado. Editar/Eliminar locales solo si la sombra NO existe (borrador puro).

Detectar: cualquier action local que escriba `status` cuando la entidad ya tiene shadow emitida = bug fiscal latente.
