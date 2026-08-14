---
title: sin Account Tax IDs, la factura de Stripe sale sin el NIF del emisor
date: 2026-08-14
source: claude-code-session
tags: [stripe, facturacion, fiscal, espana, facturaia]
---

Que la cuenta esté verificada entera y Stripe Tax activo con registro en ES **no** implica
que las facturas que emites lleven tu NIF. Lo deciden `GET /v1/tax_ids` (los *Account Tax
IDs*, puede devolver 0) y `account.settings.invoices.default_account_tax_ids` (puede ser
`null`, y entonces no se adjunta ninguno).

**Hay DOS pantallas de NIF y es fácil rellenar la que no es** (14-ago, costó una vuelta):
*Settings → Tax details* (`/settings/taxation`) es el NIF con el que Stripe te identifica y
factura **a ti** sus comisiones — lo dice su propio texto, «your monthly VAT invoices». El
que se imprime en **tus** facturas es otra colección, la de `/v1/tax_ids`. Rellenar la
primera deja la segunda a cero.

Crear el tax ID **sí** se puede por API: `POST /v1/tax_ids` con `type=es_cif`. Marcarlo por
defecto **no**: `POST /v1/accounts/<la propia>` responde «you may only use it on connected
accounts». Ese clic es de panel, en Billing → Invoices.

Comprobable en solo lectura antes de cobrar a nadie: portal de cliente
(`/v1/billing_portal/configurations`), numeración (`customer.invoice_prefix`) y si prod va
en live. Lo que **no** se ve por API: la dirección del emisor (`company.address` viene
vacía aunque la cuenta esté verificada, y el domicilio es obligatorio en factura española)
ni cómo queda el PDF. Emitir la de prueba **en modo test**: en live quema el primer número
de tu serie para luego anularlo. Ver [[stripe-aplica-reverse-charge-sin-comprobar-que-tu-estes-en-el-roi]]
