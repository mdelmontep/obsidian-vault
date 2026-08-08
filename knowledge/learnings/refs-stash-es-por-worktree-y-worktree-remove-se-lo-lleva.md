---
title: refs/stash es POR WORKTREE, así que `git worktree remove` puede destruir un stash
date: 2026-08-08
source: claude-code-session
tags: [git, worktrees, stash, sesiones-paralelas]
---

`refs/stash` es una **ref por worktree**, no del repositorio. Cada worktree tiene su propia pila:
`git stash list` da resultados DISTINTOS según desde dónde lo corras, y `git worktree remove` se
lleva los refs de ese worktree — **con lo stasheado dentro**.

Cómo se detecta: el mismo `git stash show --stat "stash@{0}"` daba 1 fichero desde el worktree y 5
ficheros completamente distintos desde el repo raíz, con el mismo mensaje en los dos (`On main:
<etiqueta>`). Parece que la lista «cambió»; en realidad son dos pilas.

**Antes de `git worktree remove`: `git -C <worktree> stash list`.** Si hay algo, sacarlo a un patch
(`git stash show -p` a fichero) o aplicarlo — no se recupera desde el repo raíz ni con `git fsck`
cómodamente, porque el ref colgaba del worktree borrado.

Segundo aprendizaje del mismo caso: **no fiarse de la etiqueta de un stash para decidir si sobra.**
Uno llamado `restos-obsoletos-rejilla-#1538` tenía 78 líneas de CSS responsive razonado que no
estaban en ninguna rama; el del repo raíz, con la MISMA etiqueta, sí era obsoleto de verdad. Mirar el
contenido, siempre.

Ver [[triaje-seguro-ramas-worktrees-sesiones-paralelas]] · [[git-stash-sin-u-deja-untracked-y-hook-falla]]
