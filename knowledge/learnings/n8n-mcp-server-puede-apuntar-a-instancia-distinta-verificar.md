---
title: n8n mcp server puede apuntar a instancia distinta — verificar antes de operar
date: 2026-05-22
source: claude-code-session
tags: [n8n, mcp, infra]
---

Dos MCP servers `n8n-tecnocloud` y `n8n-simarro` configurados en Claude Code apuntaban a `n8n.agentesia.world` (instancia vieja). El workflow `pqSWkDIHqmSVHotB` (FacturaIA) vivía en `n8n.tufacturaia.com` (instancia nueva). Ambos MCPs devolvieron 404 `Workflow not found or you don't have permission`, lo que parece error de permisos pero es de instancia.

**Verificar antes de operar**:
- Mirar config del MCP server (URL real) o `search_workflows` con query del workflow esperado — si no aparece, probable que el MCP apunte a otra instancia.
- Memoria del agente lista API keys por URL ([[reference_n8n_api_key_tufacturaia]] + [[reference_n8n_api_key]]).

**Workaround sin MCP**: `curl` directo a `/api/v1/workflows/{id}` con `X-N8N-API-KEY`. Para PUT, filtrar `settings` a whitelist + strip top-level read-only fields ([[n8n-api-put-workflows-rechaza-settings-desconocidos]]).
