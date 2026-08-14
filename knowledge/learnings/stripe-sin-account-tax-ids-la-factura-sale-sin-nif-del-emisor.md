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

Comprobable en solo lectura: portal de cliente (`/v1/billing_portal/configurations`),
numeración (`customer.invoice_prefix`) y si prod va en live.

**Dónde NO sirve la API, y engaña si insistes** (afirmado dos veces mal el 14-ago, y luego
desmentido por el PDF): `company.address` de tu propia cuenta viene **siempre vacío**,
esté puesto o no — el PDF de prueba mostró el domicilio completo mientras la API lo daba
por ausente. Con ese campo no se puede concluir nada.

**Lo que sí quedó demostrado emitiendo una factura de prueba**: con el tax ID creado pero
sin marcar como predeterminado, la factura finalizada sale con `account_tax_ids: null` y
**el PDF no lleva el NIF del emisor**. Crear el tax ID no basta; hay que fijarlo por
defecto (panel) o pasarlo por código en cada factura.

Corolario del mismo experimento: **la sandbox tiene su propia configuración** (sus tax IDs,
su registro fiscal, su dirección), así que un PDF de test no prueba nada sobre el de live
salvo que replique los ajustes. Y en live no se prueba: quemarías el primer número de tu
serie para luego anularlo. Ver [[stripe-aplica-reverse-charge-sin-comprobar-que-tu-estes-en-el-roi]]
