---
title: extractError debe gestionar error como objeto anidado
date: 2026-05-20
source: claude-code-session
tags: [error-handling, http, api-clients]
---

## Patrón
APIs modernas (Stripe, FacturaIA, OpenAI) devuelven errores con shape:
```json
{ "error": { "type": "validation_error", "message": "...", "param": "...", "request_id": "..." } }
```

## Gotcha
`String(body.error)` cuando `error` es un objeto → `"[object Object]"`. Visto en producción 2026-05-20: user veía "no se puede crear factura: [object Object]" sin pista de la causa real (NIF faltaba).

## Patrón correcto
```ts
function extractError(body: unknown, status: number): string {
  if (body && typeof body === 'object') {
    const inner = (body as { error?: unknown }).error
    if (typeof inner === 'string' && inner.trim()) return inner
    if (inner && typeof inner === 'object') {
      const msg = (inner as { message?: unknown }).message
      if (typeof msg === 'string' && msg.trim()) return msg
    }
    try { return `HTTP ${status}: ${JSON.stringify(body)}` } catch {}
  }
  if (typeof body === 'string' && body.trim()) return body
  return `HTTP ${status}`
}
```

## Cuándo aplicar
Cualquier `fetch` / `openapi-fetch` / cliente HTTP propio donde el error se propaga al user final.
