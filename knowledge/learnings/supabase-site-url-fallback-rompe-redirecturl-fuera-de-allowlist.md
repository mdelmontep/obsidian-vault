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

Sin dashboard (21-ago-2026, facturaia): `GET`/`PATCH https://api.supabase.com/v1/projects/<ref>/config/auth` con el token del CLI (en macOS, `security find-generic-password -s "Supabase CLI" -w`). **`uri_allow_list` es un CSV que se reemplaza entero**: leer, añadir y reenviar la lista completa, o borras las que había — mismo patrón que [[put-objeto-completo-borra-campos-no-mapeados]]. Confirmar con un GET posterior, no con el 200 del PATCH.

Anti-síntoma: si redirige raro, verifica también `request.url.origin` que en contenedor Docker es `0.0.0.0:3000` interno (ver [[oauth-redirect-uri-debe-usar-request-origin-no-env-var]]).
