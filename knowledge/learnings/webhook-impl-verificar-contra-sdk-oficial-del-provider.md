---
title: implementar webhook verify — usar SDK oficial como ground truth antes de dudar del config
date: 2026-05-07
source: claude-code-session
tags: [webhooks, hmac, debugging, workflow]
---

Cuando tu impl de verificación de firma de un webhook falla con `digest_mismatch` y dudas si el bug es:

(a) tu algoritmo de HMAC (input mal formado, encoding, etc.)
(b) el secret no es el correcto
(c) el body no se lee como bytes exactos

Atajo: `npm i <provider>-sdk` y llamar `Provider.verify(body, secret, sigHeader)` con los MISMOS bytes y el MISMO secret.

- SDK dice `true` → tu impl tiene un bug. El secret y el body son correctos.
- SDK dice `false` → o el secret es otro o el body se modificó.

Ahorra horas de probar variantes a ciegas (`HMAC(body)`, `HMAC(ts.body)`, `HMAC(body+ts)`, `SHA256(api_key+body)`, etc.). Caso real: ~6 variantes probadas hasta importar `retell-sdk` y ver `verify => true` con la API key — el bug era mío (firmaba sobre body solo, no body+ts).

También sirve para reverse-engineer el algoritmo: leer `node_modules/<provider>-sdk/.../webhook_auth.js` te da la fórmula exacta sin esperar la docs.
