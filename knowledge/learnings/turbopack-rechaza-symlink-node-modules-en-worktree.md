---
title: turbopack rechaza node_modules symlinkeado en un worktree (tsc/vitest sí lo aceptan)
date: 2026-06-21
source: claude-code-session
tags: [nextjs, turbopack, worktree, git]
---

En un `git worktree` nuevo, enlazar deps con `ln -s …/repo/node_modules node_modules`
hace funcionar `tsc --noEmit` y `vitest`, pero **`next build` (Turbopack) aborta**:
`FATAL … Symlink [project]/node_modules is invalid, it points out of the filesystem root`.

El engaño es que tsc/vitest no tocan Turbopack, así que pasan verde con el symlink y
solo el build/dev lo destapa.

**Fix rápido** (2026-06-24): crea el worktree en el MISMO volumen que el repo y
`cp -al repo/node_modules node_modules` (hardlinks: instantáneo, 0 disco extra, Turbopack
OK). El symlink solo revienta si cruza filesystem root (`/private/tmp` ↔ `/Users`).
`npm install` real (~1-2 min + disco) solo si no puedes co-ubicar el worktree.

Ver [[triaje-seguro-ramas-worktrees-sesiones-paralelas]] · [[worktree-facturaia-build-supabase]].
