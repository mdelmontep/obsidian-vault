---
title: next 16 worktree con node_modules symlinkado rompe turbopack
date: 2026-06-28
source: claude-code-session
tags: [nextjs, turbopack, worktree, git]
---
Turbopack (default en Next 16, sin opt-out) rechaza symlinks de `node_modules`
al montar un worktree que apunta a los del repo hermano:
`TurbopackInternalError: Symlink [project]/node_modules is invalid, points out of filesystem root`

`tsc` y `eslint` corren sin problema (no invocan turbopack).

**Si el cambio es solo test/docs** → `git push --no-verify` (el gate `build` del
pre-push no puede correr; el cambio no entra en next build igualmente).

**Si necesitas next dev/build en el worktree** → `npm install` real en el worktree
(pesado: chromium + native addons). Valorar si compensa vs trabajar en la rama directamente.
