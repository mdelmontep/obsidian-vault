---
title: "Supabase: mint access_token de un usuario sin su password (generate_link + verify)"
date: 2026-06-11
source: facturaia PR #205 smoke Bearer
tags: [supabase, auth, testing, smoke]
---

Para smokes/tests que necesitan un JWT real de un usuario concreto sin conocer ni resetear su password:

1. `POST /auth/v1/admin/generate_link` (service role) con `{"type":"magiclink","email":"..."}` → devuelve `hashed_token`. No dispara SMTP.
2. `POST /auth/v1/verify` (anon key) con `{"type":"magiclink","token_hash":"<hashed_token>"}` → devuelve `access_token` + `refresh_token` del usuario.

Para smoke de UI (Playwright contra la app Next): inyectar la sesión como cookie
`sb-<ref>-auth-token` = `base64-` + base64URL(JSON de la session); si supera 3180 chars,
trocear en `sb-<ref>-auth-token.0`, `.1`... Lo más robusto: reusar las utils de la propia
lib — `stringToBase64URL` + `createChunks` de `@supabase/ssr/dist/main/utils/` — en vez de
reimplementar el encoding (en ssr ≥0.10 es url-safe, no base64 estándar). Verificado ssr 0.10.2 (086).
Vale también para smoke de API por curl (no solo Playwright): mandar la cookie en el
header `Cookie:`. Verificado end-to-end contra prod 2026-06-15 (ticket conciliación 085).

Crítico cuando el usuario ya rotó su password (resetearlo se lo pisaría — caso usuario test iOS de Borja). El token resultante ejercita RLS y endpoints exactamente como el cliente real.

Relacionado: [[supabase-bypassear-plantilla-auth-con-admin-generatelink]]
