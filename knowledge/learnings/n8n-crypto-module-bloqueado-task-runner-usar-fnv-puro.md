---
title: n8n Code node bloquea `require('crypto')` — usar hash JS puro (FNV-1a)
date: 2026-05-25
source: claude-code-session
tags: [n8n, code-node, crypto, sandbox]
---

n8n task-runner (versiones recientes incluyendo 2.18.7) bloquea `require('crypto')` con error explícito `Module 'crypto' is disallowed`. Pasa silente al PUT del workflow, falla en runtime al ejecutar el Code node.

Workaround sin sysadmin: hash determinista en JS puro.

```js
function fnv32(s, seed) {
  let h = seed >>> 0;
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 0x01000193);
  }
  return (h >>> 0).toString(32).padStart(7, '0');
}
// 3 seeds = ~21 chars de entropía, charset [0-9a-v] compatible GCal eventId
const id = ('pre' + fnv32(input, 0x811c9dc5) + fnv32(input, 0xdeadbeef) + fnv32(input, 0xcafebabe)).substring(0, 30);
```

Alternativa si tienes acceso al container: env `NODE_FUNCTION_ALLOW_BUILTIN=crypto` + reinicio. En Dokploy = recreate compose.

**Alternativa real para HMAC-SHA256**: `crypto.subtle` (WebCrypto API) SÍ está disponible globalmente en el sandbox aunque `require('crypto')` esté bloqueado:
```js
const key = await crypto.subtle.importKey('raw', new TextEncoder().encode(secret), {name:'HMAC',hash:'SHA-256'}, false, ['sign']);
const sig = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(body));
const hex = Array.from(new Uint8Array(sig)).map(b=>b.toString(16).padStart(2,'0')).join('');
```
Guard típico: `if (!secret) return $input.all();` para pass-through cuando el secret no está configurado.

Casos reales: EcoBox `Reservar_cita` 2026-05-25 (FNV para idempotency). Elphis `wa-inbound-bridge` 2026-06-22 (HMAC Meta X-Hub-Signature-256 con crypto.subtle).
