---
title: mcp n8n no tiene todos los workflows — fallback rest api con x-n8n-api-key
date: 2026-05-26
source: claude-code-session
tags: [n8n, mcp, rest-api, ops]
---

Los MCP servers de n8n configurados localmente (`simarro`, `tecnocloud`) NO cubren todas las instancias de n8n. Si `get_workflow_details` devuelve "not found" en TODOS los MCP disponibles, el workflow vive en una instancia cuyo MCP no está registrado.

Fallback fiable: REST API directa de esa instancia con `X-N8N-API-KEY` header.

```
GET https://n8n.<dominio>/api/v1/workflows?active=true
Header: X-N8N-API-KEY: <key>
```

Devuelve lista con `id` real + `name` + `active`. Útil para localizar el workflow y operar `/activate`, `/deactivate` (POST), `/<id>` (PATCH/DELETE).

Caso real 2026-05-26: workflow `dqvzeyeifTcNv50u` asumido del runbook (snapshot 2026-05-12) estaba obsoleto; el real era `TJ8wDqH4ok6LHUrB` "Email Polling - FacturaIA" en n8n.tufacturaia.com — localizado vía REST. API keys de n8n.tufacturaia.com y n8n.agentesia.world ya están en memoria del agent.

Regla: los runbooks con IDs n8n quedan stale rápido. Si el MCP no lo conoce, REST primero, no asumir.
