---
title: npm run build mientras next dev sigue vivo rompe los chunks del dev server
date: 2026-07-03
source: claude-code-session
tags: [nextjs, dev-server, gotcha, qa]
---

`next dev` y `next build` comparten `.next/` por defecto. Si hay un `next dev`
corriendo (p. ej. dejado por otra sesión/el usuario) y lanzas `npm run build`
para el pre-commit gate en el mismo repo, el build pisa el manifest de chunks
del dev server a medio servir.

Síntoma en el navegador (no parece un problema de build): la app carga a medias,
queda en "Cargando…" indefinido, consola con `Refused to execute script ...
MIME type ('text/plain')` + 404/`ERR_ABORTED` en `_next/static/chunks/*.js`.
Parece un bug de la feature que estás probando — no lo es.

Fix: matar el `next dev` viejo, `rm -rf .next` si quedó a medias, y relanzarlo
limpio antes de hacer QA visual. Regla general: **no mezcles `build` y `dev`
en el mismo working tree activo** — usa un worktree separado para el pre-commit
gate si el dev server debe seguir vivo para QA.

Actualizado 2026-09-23 (Next 16.3): `next dev` ya compila en `.next/dev`, aislado; quien se rompe
ahora es `next start`. El pre-push de facturaia hace `next build` sobre `.next` y pisa el bundle de
un `dev-staging.sh build` del mismo worktree: el candado de permisos no encuentra `#login-email`.
Fix: para el push, servir con `next dev` (`PORT=3003 scripts/dev-staging.sh`).

Relacionado: [[next-build-lock-huerfano-hace-fallar-pre-push-hook]].
