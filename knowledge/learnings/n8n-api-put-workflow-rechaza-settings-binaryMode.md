---
title: n8n REST API PUT workflow rechaza settings.binaryMode (HTTP 400)
date: 2026-05-30
source: claude-code-session
tags: [n8n, api, gotcha]
---

PUT /api/v1/workflows/{id} sigue OpenAPI strict: `settings` solo admite
`executionOrder`, `callerPolicy`, `saveDataErrorExecution`,
`saveDataSuccessExecution`, `saveExecutionProgress`, `saveManualExecutions`,
`timezone`, `executionTimeout`. El panel UI guarda `binaryMode` y otros
extras, pero la API rechaza con `request/body/settings must NOT have
additional properties`.

Cuando descargas un workflow con GET y lo reenvías con PUT, el settings
viene con campos huérfanos. Strip explícito antes:

```bash
jq '{name, nodes, connections, settings: {executionOrder, callerPolicy}}'
```

Whitelist explícita, no copy-through. Mismo patrón probablemente aplica
a otros endpoints public API.

Ver [[n8n-public-api-no-permite-update-credentials-recrear-y-repuntar]].
