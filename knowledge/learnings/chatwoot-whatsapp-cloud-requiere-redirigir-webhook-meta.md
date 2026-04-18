---
title: chatwoot whatsapp cloud requiere redirigir webhook de meta
date: 2026-04-16
source: claude-code-session
tags: [chatwoot, whatsapp, meta, webhook, migración]
---

Al migrar de "n8n recibe WhatsApp directo" a "Chatwoot como hub WhatsApp Cloud", hay que redirigir el webhook en Meta Developer Console. Sin este paso, los mensajes siguen llegando al destino anterior y Chatwoot muestra 0 conversaciones.

## Checklist

1. Ir a [developers.facebook.com](https://developers.facebook.com) → app → WhatsApp → Configuration
2. En Webhook:
   - **Callback URL**: `https://<chatwoot>/webhooks/whatsapp/<+phone>`
   - **Verify Token**: el que Chatwoot genera al crear el inbox WhatsApp Cloud
3. Dar a "Verificar y guardar"
4. Suscribirse al campo **messages**

## Datos que Chatwoot muestra al crear el inbox

Chatwoot genera la URL de callback y el verify token automáticamente. Aparecen en la pantalla de confirmación tras crear el inbox WhatsApp Cloud. Copiarlos tal cual a Meta.

## Nota

El token de Meta (Clave de API en Chatwoot) debe ser un **permanent token**, no el temporal de 24h. Se genera en Meta Business Settings → System Users.
