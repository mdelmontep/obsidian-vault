---
title: chatwoot agent bot debe asignarse al inbox correcto
date: 2026-04-16
source: claude-code-session
tags: [chatwoot, agent-bot, inbox, migración]
---

Al crear un inbox WhatsApp Cloud nuevo en Chatwoot (ej: id=2), el Agent Bot puede quedar asignado al inbox anterior (ej: id=1 API). El workflow no ejecuta ninguna vez — 0 ejecuciones en n8n — porque los mensajes llegan al inbox nuevo pero el bot escucha en el viejo.

## Diagnóstico

- `GET /api/v1/accounts/1/inboxes` → ver qué inbox tiene `channel_type: Channel::Whatsapp`
- Verificar que el Agent Bot está asignado al inbox correcto

## Fix

```bash
curl -X POST "https://<chatwoot>/api/v1/accounts/1/inboxes/<inbox_id>/set_agent_bot" \
  -H "api_access_token: <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"agent_bot": <bot_id>}'
```

## Contexto

Ocurrió al migrar el ChatBOT mejorado a Tecnocloud. Se creó el Agent Bot y se asignó al inbox 1 (API viejo). Luego se creó el inbox WhatsApp Cloud (id=2), pero el bot seguía apuntando al 1. Síntoma: "he enviado un mensaje y no ejecuta".
