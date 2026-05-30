---
title: n8n public api put workflow rechaza settings con keys extra del get previo
date: 2026-05-30
source: claude-code-session
tags: [n8n, api]
---

`PUT /api/v1/workflows/:id` responde `400 request/body/settings must NOT have additional properties` si el body incluye `callerPolicy` o `binaryMode` — aunque vinieran del GET previo del mismo workflow. El schema PUT solo acepta `executionOrder`.

Filtrar antes del PUT:
```py
body['settings'] = {'executionOrder': d.get('settings',{}).get('executionOrder','v1')}
```

n8n re-aplica `callerPolicy`/`binaryMode`/etc del estado anterior — no se pierden. Solo hay que omitirlos del payload de update. Mismo patrón en Content-Type: el endpoint exige `application/json` con body explícito (`-d '{}'`) incluso para `/activate` y `/deactivate`.
