---
title: "Supabase: mint access_token de un usuario sin su password (generate_link + verify)"
date: 2026-06-11
source: facturaia PR #205 smoke Bearer
tags: [supabase, auth, testing, smoke]
---

Para smokes/tests que necesitan un JWT real de un usuario concreto sin conocer ni resetear su password:

1. `POST /auth/v1/admin/generate_link` (service role) con `{"type":"magiclink","email":"..."}` → devuelve `hashed_token`. No dispara SMTP.
2. `POST /auth/v1/verify` (anon key) con `{"type":"magiclink","token_hash":"<hashed_token>"}` → devuelve `access_token` + `refresh_token` del usuario.

Para smoke de UI (Playwright contra la app Next): NO reimplementes el encoding de la
cookie. Deja que la propia lib lo genere — `createServerClient(url, anon, { cookies: {
getAll:()=>[], setAll:(c)=>captured.push(...c) } })` + `auth.setSession({access_token,
refresh_token})` → `captured` trae las cookies con el formato EXACTO del app (nombre
`sb-<ref>-auth-token`, chunking incluido). Luego `ctx.addCookies` con el domain del target
(localhost → `secure:false`; prod → `secure:true`, `sameSite:'Lax'`). Verificado 3× esta
sesión (ssr 0.10.2, localhost + prod). Vale también para API por curl: mandar la cookie en
header `Cookie:`. Verificado E2E contra prod 2026-06-15 (085) y 2026-06-17 (presupuesto edit).

Crítico cuando el usuario ya rotó su password (resetearlo se lo pisaría — caso usuario test iOS de Borja). El token resultante ejercita RLS y endpoints exactamente como el cliente real.

Relacionado: [[supabase-bypassear-plantilla-auth-con-admin-generatelink]]
