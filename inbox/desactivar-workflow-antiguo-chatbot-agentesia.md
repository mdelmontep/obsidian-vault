---
title: desactivar workflow antiguo ChatBOT - Agentesia y borrar inbox API
date: 2026-04-16
source: claude-code-session
tags: [inbox, pendiente, agentesia, n8n, chatwoot, limpieza]
---

El workflow antiguo `ChatBOT - Agentesia` (id `enVlCyi7McKfwkRQ`) en `n8n.agentesia.madrid` ha sido reemplazado por `ChatBOT mejorado` (id `89B9QN23hOHDq6oP`) que usa Chatwoot como hub de WhatsApp.

Pendientes una vez validado el nuevo workflow:

1. Desactivar `enVlCyi7McKfwkRQ` vía `POST /api/v1/workflows/enVlCyi7McKfwkRQ/deactivate`
2. Borrar el inbox API viejo en Chatwoot (el que usaba webhook directo a n8n en vez de Chatwoot como hub)
3. Verificar que no hay otros workflows o integraciones que dependan del viejo

No borrar el workflow viejo — solo desactivar. Puede servir como referencia.

## Tecnocloud — misma situación

El workflow viejo `Main ChatBOT - Chatwoot` (id `9JTGHnge2R9mAUiV`, 73 nodos) en `n8ntecno.tecnocloud.es` ya está desactivado. Ha sido reemplazado por `Chatbot - FINAL` (id `LirbVJ9oIvLGENUQ`, 46 nodos). Pendiente: verificar que no hay dependencias y considerar borrar el inbox API viejo (id=1 `Whatsapp BOT` tipo `Channel::Api`).
