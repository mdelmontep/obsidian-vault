---
title: supabase site url es fallback silencioso si redirectto no está en allowlist
date: 2026-05-26
source: claude-code-session
tags: [supabase, auth, gotcha]
---

Síntoma: enlaces de reset/magic-link en prod apuntan a `0.0.0.0:3000` aunque el cliente envía `redirectTo: https://app.X.com/...` correcto. Causa: el `Site URL` de Supabase es config dev olvidada (`http://0.0.0.0:3000`). Cuando el `redirectTo` NO está en la allowlist `Redirect URLs`, Supabase lo descarta y usa Site URL. Silencioso — no error, no log.

Fix: Dashboard → Authentication → URL Configuration:
- Site URL = dominio prod real (p.ej. `https://app.tufacturaia.com`)
- Redirect URLs = `https://prod.com/**` + `http://localhost:3000/**` (dev)

Anti-síntoma: si redirige raro, verifica también `request.url.origin` que en contenedor Docker es `0.0.0.0:3000` interno (ver [[oauth-redirect-uri-debe-usar-request-origin-no-env-var]]).
