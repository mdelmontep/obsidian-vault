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

**Variante (2026-07-22):** matar `next dev` con `pkill`/`kill` mientras está regenerando ese fichero lo deja a medias (no stale, CORRUPTO): errores de sintaxis reales tipo `Declaration or statement expected` / `Unterminated string literal` en `.next/dev/types/validator.ts`. El pre-commit hook (typecheck) lo bloquea pensando que es tu código. Fix: `rm -rf .next` en ese worktree y reintentar el commit — no hace falta tocar el código.
