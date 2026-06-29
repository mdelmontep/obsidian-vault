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

Ver [[whatsapp-diagnosticar-numero-waba-por-graph-api]].
