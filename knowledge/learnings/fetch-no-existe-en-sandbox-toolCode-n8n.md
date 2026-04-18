---
title: fetch no existe en el sandbox de toolCode de n8n
date: 2026-04-17
source: claude-code-session
tags: [n8n, toolCode, http]
---

El runtime de nodos Code (`@n8n/n8n-nodes-langchain.toolCode`) en n8n no expone la API `fetch`. Intentar usarla lanza `ReferenceError: fetch is not defined`.

## Alternativa

Usar `this.helpers.httpRequest`:

```javascript
const body = await this.helpers.httpRequest({
  method: 'POST',
  url: 'https://example.com/api',
  headers: { 'Content-Type': 'application/json' },
  body: { key: 'value' },
  json: true,
});
```

Funciona correctamente en toolCode siempre que no se combine con `$fromAI()`, que rompe el contexto de ejecución (ver learning: `$fromAI en toolCode lanza no-execution-data-available`).

## Cuándo aplica

Cualquier nodo toolCode que necesite hacer llamadas HTTP. No asumir que el sandbox de n8n es un entorno Node.js estándar — `fetch`, `axios`, y `require()` no están disponibles.
