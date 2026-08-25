---
title: cookie de @supabase/ssr fabricada a mano cuando no hay node para el smoke
date: 2026-08-25
source: facturaia
tags: [supabase, auth, smoke, agent-browser]
---
Variante sin Node/Playwright de [[supabase-mint-access-token-sin-password-via-generate-link]]: si la
app usa code-flow, abrir el `action_link` de `generate_link` NO inicia sesión (los tokens van en el
hash `#access_token=…` y la app espera `?code=`). Camino verificado contra prod (25-ago-2026):
1. `POST /auth/v1/admin/generate_link` (service role) → `action_link`. Es de UN uso.
2. `curl -s -o /dev/null -w '%{redirect_url}' "$action_link"` → el redirect trae los tokens en el hash.
3. Cookie `sb-<ref>-auth-token` = `base64-` + base64url SIN padding del JSON de sesión
   (`{access_token, refresh_token, expires_at, token_type:"bearer", user}`). Es formato interno de
   @supabase/ssr y puede cambiar entre versiones: con Node a mano, mejor generarla con la lib.
4. Con agent-browser, setear la cookie y verificar por `eval fetch('/api/…')`, no por UI.
Passwords ni tocarlos: esto existe justo para no teclear ninguno.
