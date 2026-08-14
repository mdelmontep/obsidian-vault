---
title: stripe retiró invoice.subscription; el id vive en parent.subscription_details
date: 2026-08-14
source: claude-code-session
tags: [stripe, webhook, api-version, facturaia]
---

`invoice.subscription` (campo plano) desapareció del objeto Invoice en la versión de API
`2025-03-31.basil`. Hoy está en `parent.subscription_details.subscription`, con
`parent.type = 'subscription_details'`. Leer el viejo no da error: da `undefined`, y toda
la lógica que dependa de "¿de qué suscripción es esta factura?" degrada en silencio al
caso por defecto.

**Qué versión te llega de verdad**, que no es la de tu SDK ni la de la doc:
- `GET /v1/webhook_endpoints` → `api_version: null` significa "la de la cuenta", no "la última".
- `GET /v1/events` → cada evento trae el `api_version` con el que se renderizó. Eso es la medida.

(FacturaIA, 14-ago: cuenta en `2026-04-22.dahlia`, muy por delante de basil.)

**El fixture mentía y la suite verde lo tapó.** El arnés compartido de tests fabricaba
`{ id, customer, subscription }` — la forma retirada — así que 383 tests pasaban sobre un
payload que producción no manda nunca. No basta con "hay arnés": el arnés se contrasta
contra un evento real igual que el código. Ver [[webhook-impl-verificar-contra-sdk-oficial-del-provider]].
