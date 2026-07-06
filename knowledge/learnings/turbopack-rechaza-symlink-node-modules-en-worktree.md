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

**Gotcha del propio fix** (2026-07-06): si el comando `cp -al` se corta a mitad
(timeout del shell, Ctrl-C) deja una copia PARCIAL sin error visible — el conteo
de entries en la raíz de `node_modules` puede coincidir a simple vista pero
falta algún paquete anidado (p. ej. `debug` dentro de `ioredis`), y el síntoma
solo aparece más tarde como `Module not found` al arrancar `next dev`. Verificar
con `ls node_modules | wc -l` origen vs copia antes de dar la copia por buena;
si no cuadra, `rm -rf` y repetir `cp -al` completo sin interrupciones.

Ver [[triaje-seguro-ramas-worktrees-sesiones-paralelas]] · [[worktree-facturaia-build-supabase]].
