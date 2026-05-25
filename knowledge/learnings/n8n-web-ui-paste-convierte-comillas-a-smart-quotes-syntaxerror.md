---
title: pegar JS en n8n web UI puede convertir comillas a smart quotes y romper el parser
date: 2026-05-25
source: claude-code-session
tags: [n8n, gotcha, javascript]
---

Pegar JavaScript en el Code node de n8n hosted desde un chat client o doc (Notion, Slack, Claude) puede sustituir `'` ASCII por `'` Unicode (U+2019). El parser de JS de n8n revienta con SyntaxError críptico que apunta exactamente a la línea afectada.

Síntoma típico (sacado de stack trace n8n 2.15):
```
evalmachine.<anonymous>:28
  'Authorization': 'Bearer sk-proj-...'
                   ^^^^^^^^^^^^^^^^^^^^^
SyntaxError: Invalid or unexpected token
```

La línea se ve idéntica visualmente — el carácter es invisible al ojo.

Fixes:
- Borrar la línea entera en el editor de n8n y retypearla a mano (las comillas se generan ASCII).
- O migrar el secreto a `$env.VAR` (suele eliminar la string larga con comillas problemáticas).
- O usar comillas dobles `"..."` que rara vez se convierten.

Vale para cualquier `jsCode` pegado en n8n (Code node, Function node, expression).
