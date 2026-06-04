---
title: retell published flow devuelve 400 — crear flow nuevo y reasignar agente
date: 2026-06-04
source: claude-code-session
tags: [retell, conversation-flow, api]
---
`PATCH /update-conversation-flow/{id}` sobre flow publicado → 400 "Cannot update published conversation flow".
`PATCH /update-agent/{id}` sobre agente publicado → 422 "Cannot update published agent other than version title".
Fix: crear flow nuevo (`POST /create-conversation-flow`) → crear agente nuevo o versión nueva →
reasignar número (`PATCH /update-phone-number/%2B34XXX` con `inbound_agent_id`).
El agente/flow viejos quedan como rollback — no borrar hasta validar.
