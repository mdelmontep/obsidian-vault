---
title: diagnosticar estado de un número/waba de whatsapp por graph api
date: 2026-06-30
source: claude-code-session
tags: [whatsapp, meta, debug]
---
Token System User → `GET /debug_token` ve `type` y `scopes`. `subscribed_apps:[]` en el WABA = webhook sin suscribir (no recibe mensajes).

`GET /{phone_id}?fields=status,platform_type,is_on_biz_app,code_verification_status`:
- `is_on_biz_app:true` = sigue en la app WhatsApp Business del móvil (coexistencia a medias).
- `status:DISCONNECTED` + `platform_type:ON_PREMISE` = NO registrado en Cloud API.

`GET /{waba}?fields=health_status` → errores accionables:
- `141010` = negocio sin verificar → mensajería LIMITED.
- `2494160` (al crear plantilla) = WABA sin permiso para gestionar plantillas (combo no-verificado + número no onboarded).
- `2388293` (al crear plantilla) = ratio variables/palabras demasiado alto (mete más texto fijo).

Que puedas *leer* plantillas (`GET .../message_templates`) no implica poder *crearlas*.

Ver [[whatsapp-conectar-numero-propio-en-movil-a-cloud-api]].
