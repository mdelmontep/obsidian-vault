---
title: slack agentesia lab — API y bot
date: 2026-04-20
source: claude-md-migration
tags: [slack, bot, api]
---

# Slack — AgentesIA Lab

- **Escritura en canales y canvas** via Slack API con bot token (guardado en memory). Patrón: `conversations.join` para unir el bot al canal + `canvases.edit` con `changes[].operation: "insert_at_end"` y `document_content.type: "markdown"`.
- **Canvas de Tareas Pendientes** está en `#01-tareas-pendientes` — es el sitio para añadir pendientes del equipo.
- **El bot no tiene scope `groups:read`** — no puede listar canales privados, solo públicos.
