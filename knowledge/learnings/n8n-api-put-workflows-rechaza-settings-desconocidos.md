---
title: n8n api put workflows rechaza settings desconocidos
date: 2026-04-20
source: claude-code-session
tags: [n8n, api, bug]
---

Al hacer `PUT /api/v1/workflows/{id}`, solo enviar estos campos en `settings`:
- `executionOrder`
- `callerPolicy`

Campos como `binaryMode`, `availableInMCP` causan error:
> "request/body/settings must NOT have additional properties"

**Solución**: al descargar un workflow con GET y re-subirlo con PUT, filtrar settings antes:

```python
valid_settings = {}
for k in ['executionOrder', 'callerPolicy']:
    if k in settings:
        valid_settings[k] = settings[k]
```

El payload de PUT solo acepta: `name`, `nodes`, `connections`, `settings` (filtrado).
