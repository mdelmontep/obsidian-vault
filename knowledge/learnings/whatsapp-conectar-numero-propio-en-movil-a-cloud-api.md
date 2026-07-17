---
title: conectar un número de whatsapp que ya está en el móvil (business app) a cloud api
date: 2026-06-30
source: claude-code-session
tags: [whatsapp, meta, agentesia]
---
Número usado a diario en la app WhatsApp Business (`is_on_biz_app:true`) → 2 vías a Cloud API:

- **Migración** (alta por OTP SMS/llamada en Configuración de la API): pasa a `CLOUD_API`+`CONNECTED` y **lo saca del móvil**. Único camino self-service; ideal si el bot gestiona el WhatsApp por Chatwoot/n8n.
- **Coexistencia** (mantener en móvil): requiere ser **Business Solution Provider (BSP)**. La variación "Embedded Signup" NO aparece en Facebook Login for Business si no eres BSP (solo salen General/Conversions/Instagram); el error `#10` lo confirma.

El **embedded signup / `config_id`** es patrón ISV/BSP para dar de alta números de *terceros*. NO es para 1 número propio — no malgastes días montándolo.

**Migración confirmada (2026-07-17):** borrar cuenta en la app móvil (Ajustes→Cuenta→Eliminar) → añadir el número por WhatsApp Manager con OTP. Esto crea un **WABA y `phone_number_id` NUEVOS** (los del diagnóstico previo quedan stale → re-lee `GET /{waba}/phone_numbers`). Con el negocio verificado, `POST /{phone_id}/register {messaging_product,pin(6díg)}` **sí funciona por API** (contradice "SMB debe registrar por UI"). Después `POST /{app_id}/subscriptions object=whatsapp_business_account fields=messages` con app token (`app_id|app_secret`) para el webhook. Recuerda repuntar `META_APP_SECRET` de n8n al de la app suscrita (valida el HMAC entrante).

Ver [[whatsapp-diagnosticar-numero-waba-por-graph-api]] · [[whatsapp-cloud-api-vs-business-app-numero-exclusivo]].
