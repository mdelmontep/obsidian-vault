---
name: internal-fetch-res-ok-silencioso
description: fetch() interno sin !res.ok check — HTTP 4xx/5xx del callee llegan como datos válidos y el caller los ignora en silencio
metadata:
  type: feedback
---

## El patrón que falla

```ts
const res = await fetch(url, { ... })
const data = await res.json()           // 402/429/500 → data tiene el body de error
if (data.ok) { ... }                     // nunca entra → silencio
```

El `try/catch` solo captura errores de red (DNS, ECONNREFUSED, timeout). Un HTTP 402, 429 o 500 del endpoint callee llega como respuesta válida; `res.json()` parsea el body de error como si fuera datos correctos; todos los discriminadores de éxito fallan en silencio.

## Fix mínimo

```ts
const res = await fetch(url, { ... })
if (!res.ok) {
  console.error('[caller] http error from callee', { status: res.status, url })
  // tratar como fallo + mensaje al usuario si procede
  return
}
const data = await res.json()
```

## Regla

**Todo `fetch()` interno necesita DOS capas de log/guard:**
1. `try/catch` — error de red
2. `!res.ok` check — HTTP 4xx/5xx del callee

Sin la segunda, un 402/429/500 pasa como `{data}` válido. Aplica a llamadas internas (`/api/internal/*`), copiloto, voz, webhooks propios.

Ver también [[whatsapp-internal-http-discriminador-shape]]

**RECURRENCIA 2026-07-05** (`webhook/route.ts`, FacturaIA): el fetch del webhook WhatsApp a `/api/internal/whatsapp/copiloto` no comprobaba `res.status`. Bajo el rate-limit interno (429, defensa anti-bucle ~60-120 req/min), el body de error caía en la rama genérica `copiloData.error` → solo log, sin respuesta al usuario. Bot mudo bajo spam real sin explicación. Fix: capturar `res.status`, `sendText` de cortesía si es 429.
