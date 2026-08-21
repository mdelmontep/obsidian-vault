---
title: data manager ingest exige loginAccount del MCC en destinations
date: 2026-08-21
source: facturaia
tags: [google-ads, data-manager, conversiones, oauth, gotcha]
---
`POST audienceMembers:ingest` / conversiones del Data Manager API devuelve `403
PERMISSION_DENIED` si `destinations[]` solo lleva `operatingAccount`: cuando el acceso a la
cuenta operativa viene vía MCC, hay que añadir también `loginAccount: { accountType:
'GOOGLE_ADS', accountId: <login_customer_id> }` (el equivalente del header
`login-customer-id` de la API de Ads, que aquí NO existe como header).

Y antes: el token OAuth necesita el scope `datamanager` ADEMÁS de `adwords` — reacuñar el
refresh token con ambos scopes, no solo habilitar la API en el proyecto (dos 403 distintos
que se confunden: «API not enabled» vs «permission denied»).

Caso real: llave 1 de growth FacturaIA (21-ago-2026), validateOnly 200 tras añadir
loginAccount; el payload de producción (`conversiones/payload.ts`) ya lo llevaba y el script
de smoke no — de ahí la discrepancia.
