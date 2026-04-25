---
title: n8n api importar workflows json requiere archivos temporales
date: 2026-04-25
source: claude-code-session
tags: [n8n, api, workflows]
---

Los JSON de workflows n8n con nodos Code contienen caracteres de control (`\n`, `\t` en campos `jsCode`) que rompen shell escaping al pasarlos inline con curl.

## Solución

Escribir el payload con Python (`json.dump` con `ensure_ascii=True`) a `/tmp/`, luego usar `curl -d @/tmp/file.json`:

```python
import json

with open('workflow.json') as f:
    wf = json.load(f)

payload = {
    'name': wf['name'],
    'nodes': wf['nodes'],
    'connections': wf['connections'],
    'settings': wf.get('settings', {}),
}

with open('/tmp/n8n-payload.json', 'w') as f:
    json.dump(payload, f, ensure_ascii=True)
```

```bash
curl -X POST "https://n8n.example.com/api/v1/workflows" \
  -H "X-N8N-API-KEY: $KEY" \
  -H "Content-Type: application/json" \
  -d @/tmp/n8n-payload.json
```

## Parsear respuestas

Las respuestas de la API también contienen control chars (del jsCode en los nodos). Usar `json.loads(raw, strict=False)` en Python o extraer campos con `grep -o '"id":"[^"]*"'`.

Nunca usar `json.load(sys.stdin)` estricto — falla con `Invalid control character`.
