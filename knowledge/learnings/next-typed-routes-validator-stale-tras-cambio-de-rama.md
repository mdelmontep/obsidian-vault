---
title: next typed-routes validator stale tras cambiar de rama rompe el typecheck
date: 2026-06-22
source: claude-code-session
tags: [nextjs, typescript, worktree, gotcha]
---
Con typed routes, Next genera `.next/types/validator.ts` con un import por cada `route.ts`. Al cambiar de rama/worktree a una con DISTINTO set de rutas, ese fichero queda **stale** (referencia rutas que ya no existen) y `tsc --noEmit` falla con:

`Cannot find module '../../src/app/api/.../route.js' or its corresponding type declarations`

No es un error de tu código — es caché del build anterior. Pasa fácil en worktrees o tras mergear/cambiar de rama.

**Fix**: `next build` (regenera el validator para las rutas actuales) y LUEGO `tsc`. Por eso conviene el orden `build → typecheck`, no al revés, cuando acabas de cambiar de rama.
