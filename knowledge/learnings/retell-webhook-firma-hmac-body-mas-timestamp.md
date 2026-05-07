---
title: retell webhook firma HMAC sobre body+timestamp, no solo body
date: 2026-05-07
source: claude-code-session
tags: [retell, webhooks, hmac, gotcha]
---

Header `x-retell-signature: v=<unix_ms>,d=<hex_64>`. El digest `d` es:

```
HMAC-SHA256(api_key, body + String(timestamp))
```

**Concatenado sin separador**. Ni `.`, ni newline, ni nada. El timestamp es el `v=` numérico (ms) coerced a string. Replay window ±5 min.

Errores típicos que dan `digest_mismatch`:
- Firmar solo `body` (Stripe-style con timestamp aparte). No es Retell.
- Firmar `timestamp + body` o `timestamp.body`. Tampoco.
- Re-serializar el body antes de firmar. `req.text()` debe leer ANTES de cualquier `JSON.parse`.

Ground truth: `import { Retell } from "retell-sdk"; await Retell.verify(body, apiKey, sigHeader)`. Si SDK dice true y tu impl false → bug tuyo. Ver source en `node_modules/retell-sdk/lib/webhook_auth.js`.

Misma fórmula sirve para webhooks de tools (mid-call) y server-side del agente (call_started/ended/analyzed). Secret = API key del workspace.
