---
title: n8n Code sandbox no expone URLSearchParams ni URL globalmente
date: 2026-05-18
source: claude-code-session
tags: [n8n, sandbox, gotcha]
---

`new URLSearchParams({...}).toString()` tira `URLSearchParams is not defined`. Si está dentro de try/catch fail-open el error queda silente, la request HTTP nunca se hace y el flujo continúa sin contexto.

Fix: concatenar con `encodeURIComponent`:

```js
const qs = 'k=' + encodeURIComponent(v) + '&k2=' + encodeURIComponent(v2);
```

`this.helpers.httpRequest` sí está disponible. `fetch` no. Detectado en state machine bot WhatsApp TuFacturaIA (2026-05-18). Ver [[n8n]] · [[n8n-sessionid-sin-plus-vs-endpoint-e164]]
