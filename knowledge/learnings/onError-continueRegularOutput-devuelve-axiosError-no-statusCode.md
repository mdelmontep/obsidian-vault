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

## Corolario: convertir HTTP node → Code node pierde el manejo de error tipado

Al convertir un HTTP Request node (con Never Error/Full Response) a **Code node**
(p.ej. para firmar HMAC), hay que **re-implementar** la captura del body de error.
Si el Code llama `this.helpers.httpRequest` y deja que lance en non-2xx, la salida
de error solo lleva `{error: "status code XXX"}` — sin `error_code`/`message` del
backend. Las ramas IF downstream que leen `$json.error_code` quedan **muertas** y
todo cae al mensaje genérico. Caso 2026-06-02 (TuFacturaIA, mismo refactor Fase
2.15 que [[n8n-code-node-no-interpola-llaves-dobles]]): nodo devuelve el body con
`neverError: true` (`returnFullResponse` + chequear `statusCode>=400` sin relanzar)
y "Generacion OK?" (`success===true`) enruta a las ramas tipadas.

