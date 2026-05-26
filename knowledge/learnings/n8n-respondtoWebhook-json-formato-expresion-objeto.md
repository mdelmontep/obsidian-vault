---
title: n8n respondToWebhook JSON mode requiere expresión objeto, no literal
date: 2026-05-25
source: claude-code-session
tags: [n8n, webhook, expressions]
---

Con `respondWith: json`, el campo `responseBody` espera una expresión que evalúe a un objeto JS, no a un literal de objeto pseudo-JSON.

❌ Rompe con "Invalid JSON in 'Response Body' field":
```
={ "response": "x" + $('Edit').item.json.name }
```

✅ Funciona — paréntesis para que `{...}` se interprete como objeto-expresión, no como bloque:
```
={{ ({ response: 'x' + $('Edit').item.json.name, confirmation_text: 'y' }) }}
```

El `={{ ... }}` declara expresión n8n, `(...)` fuerza al motor JS a tratar la llave como object literal y no como block statement.

Caso real: EcoBox `Reservar_cita` Respond OK 2026-05-25 — broken por iteraciones consecutivas de PUT que sobreescribían el formato correcto. Smoke valida fácil: si tras un PUT el smoke devuelve vacío en lugar de JSON, casi siempre es esto.
