---
title: gh pr merge desde un worktree falla DESPUÉS de mergear en remoto — verifica antes de reintentar
date: 2026-07-29
source: claude-code-session
tags: [git, worktree, gh, github]
---

`gh pr merge <N> --squash --delete-branch` lanzado desde un worktree termina con:

    failed to run git: fatal: 'main' is already used by worktree at '/…/repo'

Parece que el merge no se hizo. **Se hizo.** `gh` mergea vía API primero y solo
después intenta el checkout local de la rama base para actualizarla — y ese paso
es el que revienta, porque `main` está ocupado por el checkout principal.

Reintentar crea ruido (el PR ya está MERGED) o confunde. Antes de repetir nada:

    gh pr view <N> --json state,mergedAt

Si dice `MERGED`, solo falta limpiar: `git worktree remove`, borrar la rama local
y remota, y actualizar `main` desde su propio checkout.

Ver [[triaje-seguro-ramas-worktrees-sesiones-paralelas]] · [[turbopack-rechaza-symlink-node-modules-en-worktree]].
