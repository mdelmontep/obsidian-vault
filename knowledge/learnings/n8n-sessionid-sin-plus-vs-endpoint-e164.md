---
title: sessionId de n8n viene sin + pero endpoints E.164 estrictos lo exigen
date: 2026-05-18
source: claude-code-session
tags: [n8n, validation, e164, gotcha]
---

Workflow normaliza phone como solo dígitos (`34617314938`). Endpoint con `z.string().regex(/^\+[1-9]\d{7,14}$/)` devuelve 400. Si Code n8n usa try/catch fail-open → persist nunca ocurre, sin alerta. Bug silente clásico.

Antes de POST a endpoint E.164 estricto:

```js
const raw = (parsed.normalized_phone || parsed.sessionId || '').trim();
const phone = raw && !raw.startsWith('+') ? '+' + raw.replace(/^\++/, '') : raw;
```

Ver [[n8n]] · [[n8n-code-sandbox-no-tiene-urlsearchparams]]
