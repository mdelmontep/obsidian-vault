---
title: inventario callers auth en n8n no basta con filtrar nodos de tipo .code
date: 2026-05-30
source: claude-code-session
tags: [n8n, migracion, auth]
---

Al migrar callers que usan un header de auth (e.g. `x-service-key` → HMAC), filtrar `n['type'].endswith('.code')` deja fuera:

1. **`@n8n/n8n-nodes-langchain.toolCode`** — tools llamables por AI Agent. Termina en `.toolCode`, no en `.code`.
2. **`n8n-nodes-base.httpRequest`** — header en `parameters.headerParameters.parameters[]`, no en jsCode. Hay que inspeccionar `parameters` JSON-serializado.

Caso real Receptor v2 (2026-05-30): mi 1ª pasada migró 17/42. Audit con agente descubrió 18 HTTP + 5 toolCode restantes. Fix de inventario: `'x-service-key' in json.dumps(parameters).lower()` cubre todos los tipos. Migrar HTTP → convertir a Code con `signedHttpRequest` (preserva nombre + connections, downstream refs `$('NodeName')` siguen funcionando).
