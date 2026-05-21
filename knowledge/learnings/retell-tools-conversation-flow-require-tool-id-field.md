---
title: retell custom tools en conversation flow requieren tool_id explícito
date: 2026-05-22
source: claude-code-session
tags: [retell, conversation-flow, api]
---

`POST /update-conversation-flow` con tools sin `tool_id` devuelve 400: `request/body/tools/0 must have required property 'tool_id'`.

`tool_id` es identificador interno único (alfanumérico+underscore). Distinto del `name` (display que ve el LLM).

Shape válida del tool:
```json
{
  "tool_id": "tool_reservar_cita",
  "type": "custom",
  "name": "Reservar_cita",
  "description": "...",
  "url": "https://...",
  "method": "POST",
  "timeout_ms": 6000,
  "speak_during_execution": true,
  "execution_message_description": "...",
  "parameters": { "type": "object", "required": [...], "properties": {...} }
}
```

En subagent nodes, `tool_ids: ["tool_reservar_cita"]` referencia por `tool_id`, no por `name`.

Convención: `tool_<funcion_snake_case>` por consistencia.
