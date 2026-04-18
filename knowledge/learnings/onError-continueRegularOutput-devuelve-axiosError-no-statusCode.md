---
title: onError continueRegularOutput devuelve axiosError no statusCode
date: 2026-04-18
source: claude-code-session
tags: [n8n, workflow, bug]
---

Con `onError: continueRegularOutput` en un HTTP Request node, las respuestas non-2xx **NO** llegan como `{statusCode: 404, body: {...}}`.

Llegan como:

```json
{
  "error": {
    "message": "404 - \"{\\\"ok\\\":false,\\\"error\\\":\\\"client_not_found\\\"}\"",
    "name": "AxiosError"
  }
}
```

## Consecuencia

Si el Code node hace `item.statusCode || 200`, el status code defaulta a 200 y el error se trata como éxito. El ticket se "crea" con ticketId `N/A`.

## Fix

Parsear el status code del mensaje de error:

```javascript
if (item.error) {
  const msg = item.error.message || '';
  const codeMatch = msg.match(/^(\d{3})/);
  statusCode = codeMatch ? parseInt(codeMatch[1]) : 500;
  // Detectar errores conocidos por contenido
  if (msg.includes('client_not_found')) statusCode = 404;
}
```

Esto vale incluso con `fullResponse: true` — el wrapper de error no cambia.
