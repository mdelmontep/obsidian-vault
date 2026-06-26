---
title: smoke visual de página admin SSR sin password — sesión inyectada en playwright
date: 2026-06-26
source: claude-code-session
tags: [playwright, supabase, ssr, smoke, auth, superadmin]
---

Para hacer QA visual de una página server-rendered protegida (p.ej. `/admin/*` superadmin) en localhost SIN la contraseña del usuario:

1. `admin.auth.admin.generateLink({type:'magiclink', email})` con **service_role** → `properties.hashed_token`.
2. `anonClient.auth.verifyOtp({token_hash: hashed, type:'email'})` → `session` (access+refresh).
3. Inyectar en Playwright la cookie de `@supabase/ssr`: nombre `sb-<projectRef>-auth-token`, valor `base64-` + `base64(JSON.stringify(session))`. Si supera ~3600 chars, **partir en `.0`/`.1`** (la lib lee chunks). `context.addCookies([...])`.

Por qué cookie y no magic-link navegado: en un proyecto prod **localhost no está en la redirect-allowlist de Supabase**, así que el link `…/auth/v1/verify?redirect_to=localhost` se rechaza. Las páginas SSR leen cookies (no Bearer; el header Authorization solo aplica a `/api`).

Worktree: ejecutar el script desde dentro del worktree (sus `node_modules`); `.env.local` no viaja al worktree (gitignored) → copiarlo. Borrar el `.env.local` copiado al terminar (lleva `sk_live`). Relacionado: [[supabase-bypassear-plantilla-auth-con-admin-generatelink]].
