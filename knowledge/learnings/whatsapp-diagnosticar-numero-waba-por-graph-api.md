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
- `141006` = problema con el método de pago → `can_send_message: BLOCKED`, pero los envíos SALEN (Simarro, 14-oct). No sirve de alarma: vigilar `status`, `platform_type`, `quality_rating` e `is_on_biz_app` contra el estado anterior.
- `2494160` (al crear plantilla) = WABA sin permiso para gestionar plantillas (combo no-verificado + número no onboarded).
- `2388293` (al crear plantilla) = ratio variables/palabras demasiado alto (mete más texto fijo).

Que puedas *leer* plantillas (`GET .../message_templates`) no implica poder *crearlas*.

**Falsos negativos medidos (Simarro, 16-oct):** `GET /{waba}/subscribed_apps` → `[]` y en `health_status` la entidad APP dice «Your app is not subscribed to the message webhook»… y los entrantes llegaban a Kommo. La APP de `health_status` es la del TOKEN que pregunta, no la del BSP. La recepción solo se prueba con un mensaje real.

**Tras migrar app → Cloud API**, un móvil que tenía el chat puede mostrar «This person is no longer on WhatsApp» (incluso por `wa.me`) mientras otro dispositivo de la misma cuenta escribe sin problema: estado viejo en ese teléfono, no del número. Probar desde otro aparato antes de tocar nada.

Ver [[whatsapp-conectar-numero-propio-en-movil-a-cloud-api]].
