---
title: n8n code node sandbox no expone url global aunque crypto este permitido
date: 2026-05-30
source: claude-code-session
tags: [n8n, code-node, javascript]
---

Code node de n8n (task-runner moderno) lanza `URL is not defined` si usas `new URL(opts.url)`. `NODE_FUNCTION_ALLOW_BUILTIN=crypto` permite `require('crypto')` pero NO añade WHATWG URL al scope.

Workaround inline para parsear path+search sin lib:
```js
function _pathSearch(urlStr) {
  const m = /^https?:\/\/[^/]+(\/[^?#]*)(\?[^#]*)?/.exec(urlStr);
  return (m[1] || '/') + (m[2] || '');
}
```

Aplicable a cualquier helper que necesite firmar HMAC con `pathWithSearch`, parsear redirects, etc. Caso: helper `signedHttpRequest` migración Receptor v2.
