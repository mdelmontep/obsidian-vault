---
title: this.helpers.httpRequest con returnFullResponse sigue lanzando en non-2xx
date: 2026-04-17
source: claude-code-session
tags: [n8n, toolCode, http, error-handling]
---

En toolCode de n8n, `this.helpers.httpRequest` con `returnFullResponse: true` **no evita** que se lance una excepción en respuestas non-2xx (404, 400, 500, etc.). El status code y el body no llegan al código — la ejecución salta directamente al `catch`.

## Workaround

Usar sin `returnFullResponse` y parsear el status code desde el mensaje de error:

```javascript
try {
  const body = await this.helpers.httpRequest({
    method: 'POST',
    url: 'https://example.com/api',
    body: { ... },
    json: true,
    // NO usar returnFullResponse: true
  });
  // Solo llega aquí en 2xx
  return 'OK: ' + JSON.stringify(body);
} catch (err) {
  const msg = err.message || '';
  if (msg.includes('404')) return 'NOT_FOUND';
  if (msg.includes('400')) return 'BAD_REQUEST';
  return 'ERROR: ' + msg;
}
```

## Cuándo aplica

Cualquier toolCode que necesite distinguir entre diferentes status codes de error (ej: 404 = no encontrado vs 400 = validación vs 500 = error servidor). El patrón `msg.includes('404')` es frágil pero funcional dado que n8n incluye el status code en el mensaje de error.
