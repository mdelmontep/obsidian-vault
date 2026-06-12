---
title: n8n helpers.httpRequest lanza en 4xx sin ignoreHttpStatusErrors
date: 2026-06-12
source: claude-code-session
tags: [n8n, http-request, error-handling]
---
`this.helpers.httpRequest` en Code nodes lanza excepción en 4xx/5xx por
defecto. Un wrapper try/catch tipo `neverError` que captura y devuelve
`fetch_failed` se traga el body tipado del error (`error_code`, `message`)
— el downstream pierde el motivo real.

Fix: `ignoreHttpStatusErrors: true` + `returnFullResponse: true`, leer
`resp.statusCode` y devolver `{ __http_error: status, body }`.

Caso: TuFacturaIA cuotas — backend 402 con mensaje de límite listo para
WhatsApp degradado a `fetch_failed` → responder envió body vacío → bot mudo.
Relacionado: [[n8n-jsonbody-stringify-evita-control-characters]].
