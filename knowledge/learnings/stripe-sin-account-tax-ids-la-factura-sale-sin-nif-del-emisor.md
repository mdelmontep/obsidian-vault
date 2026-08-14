---
title: sin Account Tax IDs, la factura de Stripe sale sin el NIF del emisor
date: 2026-08-14
source: claude-code-session
tags: [stripe, facturacion, fiscal, espana, facturaia]
---

Que la cuenta de Stripe esté verificada entera (`charges_enabled`, `details_submitted`, sin
requisitos pendientes) y que Stripe Tax esté activo con registro en ES **no** implica que
las facturas que emite lleven tu NIF. Eso lo deciden otros dos campos:

- `GET /v1/tax_ids` → los *Account Tax IDs* de la cuenta. Puede devolver **0**.
- `account.settings.invoices.default_account_tax_ids` → puede ser `null`, y entonces
  ninguno se adjunta por defecto.

Con los dos vacíos, la primera factura de suscripción sale sin el CIF del emisor. Se
configura en el panel (Settings → Tax → Account tax IDs), no en código; el código solo
manda si adjunta `account_tax_ids` factura a factura (`grep account_tax_ids` para saberlo).

Comprobable por API en solo lectura antes de cobrar a nadie, junto con: el portal de
cliente (`/v1/billing_portal/configurations` → `features.subscription_update.enabled`),
la numeración (`customer.invoice_prefix`, aleatorio por cliente, no choca con tus series
fiscales) y si prod va en live (resolver los `price_...` guardados y mirar `livemode`).

Lo que **no** se ve por API: la dirección del emisor de tu propia cuenta de plataforma
(`company.address` viene vacío aunque esté verificada) ni cómo queda el PDF. Eso exige
emitir una factura de prueba y mirarla.
