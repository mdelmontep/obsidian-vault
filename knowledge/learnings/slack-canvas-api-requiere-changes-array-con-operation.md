---
title: slack canvas api requiere changes array con operation
date: 2026-04-18
source: claude-code-session
tags: [slack, api, canvas]
---

La Slack API `canvases.edit` requiere el campo `changes` como array con `operation` y `document_content`:

```json
{
  "canvas_id": "F0AT6KEJLQZ",
  "changes": [{
    "operation": "insert_at_end",
    "document_content": {
      "type": "markdown",
      "markdown": "- [ ] Tarea nueva\n"
    }
  }]
}
```

Sin el array `changes`, devuelve `"missing required field: changes"`. Pasar `document_content` y `change_type` como campos top-level no funciona.

Para leer secciones: `canvases.sections.lookup` con `criteria: { "section_types": ["any_header"] }`. El campo `contains_text` no acepta string vacío.

Requisitos del bot: scopes `canvases:write` + `channels:join` (para unirse al canal antes de editar su canvas).
