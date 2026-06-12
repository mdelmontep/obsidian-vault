---
title: supabase auth.getUser() valida en red — dedupe en el pipeline, no por helper
date: 2026-06-12
source: claude-code-session
tags: [supabase, nextjs, auth, performance]
---
`supabase.auth.getUser()` SIEMPRE hace round-trip a GoTrue (valida expiración +
revocación en el Auth server); no verifica el JWT localmente. Helpers de auth que
lo llaman cada uno por su cuenta componen N llamadas idénticas por request: en
TuFacturaIA `withApiAuth` → `isSuperadmin()` → `getOrgId()` eran 3 por cada
`/api/*` con sesión, y `/cashflow` lo pagaba ×5 endpoints en paralelo (PR #209).

Fix: el wrapper del pipeline valida UNA vez y pasa `user`/`userId` como param
opcional backward-compatible a los helpers (`isSuperadmin(knownUser?)`).

Gotcha complementario: `React.cache()` dedupea solo por render pass RSC
(layout+page comparten) — en route handlers NO memoiza (verificado docs Next
16.2 `caching-without-cache-components.md`); ahí el dedupe es el param explícito.
