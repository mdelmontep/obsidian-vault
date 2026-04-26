---
title: n8n mcp partial update valida workflow live no local
date: 2026-04-26
source: claude-code-session
tags: [n8n, mcp, api, workflows]
---

# n8n MCP `partial_update` valida contra el workflow LIVE, no el JSON local

`n8n_update_partial_workflow` funciona así:
1. Fetch del workflow actual desde n8n
2. Aplica las operaciones diff
3. Valida el resultado completo
4. Si pasa → guarda; si falla → rechaza TODO

**Problema**: si el workflow live tiene nodos IF sin `conditions.options.version: 2` o operadores unarios sin `singleValue: true`, el partial update SIEMPRE falla — aunque el cambio propuesto sea correcto y no toque esos nodos.

**Requisitos de validación para IF v2.2+ y Switch v3.2+**:
- `conditions.options` debe incluir `version: 2`, `caseSensitive: true`, `leftValue: ""`, `typeValidation: "strict"`
- Operadores unarios (`notEmpty`, `empty`, `true`, `false`) requieren `singleValue: true` y NO deben tener `rightValue`
- Operadores binarios (`equals`, `contains`) NO deben tener `singleValue: true`

**Solución**: arreglar todos los nodos en el JSON local y hacer `PUT /api/v1/workflows/{id}` directo con curl:

```bash
python3 -c "..." > /tmp/payload.json  # fix todos los nodos + generar payload
curl -X PUT "https://n8n.domain/api/v1/workflows/{id}" \
  -H "Content-Type: application/json" \
  -H "X-N8N-API-KEY: $KEY" \
  -d @/tmp/payload.json
```

El PUT requiere `name` en el payload (además de `nodes`, `connections`, `settings`).
