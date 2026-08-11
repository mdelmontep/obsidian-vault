---
title: retell published flow devuelve 400 — versionar in-place, no crear flow nuevo
date: 2026-06-04
source: claude-code-session
tags: [retell, conversation-flow, api]
---
`PATCH /update-conversation-flow/{id}` sobre flow publicado → 400 "Cannot update published conversation flow".
`PATCH /update-agent/{id}` sobre agente publicado → 422 "Cannot update published agent other than version title".

**Corrección 12-ago**: no hace falta crear IDs nuevos. El flujo correcto y más simple, confirmado
varias veces en la misma sesión sin romper nada:
1. `POST /create-agent-version/{agent_id}` con `{"base_version": N}` — crea automáticamente una
   nueva versión draft del AGENTE **y** del conversation flow asociado (mismo `conversation_flow_id`,
   versión incrementada en ambos).
2. `PATCH /update-conversation-flow/{id}` sobre esa nueva versión draft (`is_published:false`) — sí
   se deja editar.
3. `POST /publish-agent/{agent_id}` con `{"version": N+1}` — publica ambos. Verificar con
   `GET /get-agent/{id}?version=N+1` → `is_published:true`.

Antes de publicar, verificar integridad (todo `destination_node_id` de cada edge debe existir como
`id` de algún nodo, y diff contra la versión anterior para confirmar que no cambió nada fuera de lo
tocado) — evita descubrir un nodo roto ya en producción real.

El número de teléfono no necesita reasignación si apunta al `agent_id` sin fijar `agent_version`
explícito: usa automáticamente la última versión PUBLICADA (no la última draft).
