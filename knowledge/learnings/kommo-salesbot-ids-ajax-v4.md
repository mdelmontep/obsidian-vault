---
title: kommo salesbot ids — endpoint real es /ajax/v4/bots/ no /api/v2/salesbot
date: 2026-04-28
source: claude-code-session
tags: [kommo, salesbot, api]
---

`GET /api/v2/salesbot` devuelve 404 desde fuera (y desde consola del navegador).
El endpoint que usa la UI internamente es `/ajax/v4/bots/`.

**Cómo obtener IDs**: ejecutar desde consola del navegador estando logado en la cuenta Kommo:

```javascript
fetch('/ajax/v4/bots/?limit=100').then(r=>r.json()).then(d=>console.log(JSON.stringify(d,null,2)))
```

Devuelve `_embedded.items[]` con `id` y `name` de cada bot.
El POST a `/api/v2/salesbot` también es privado (error_code 110) — import solo via UI.
