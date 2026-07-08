---
title: tras un crash, reconstruir el trabajo en vuelo desde worktrees + stash + mtime
date: 2026-07-08
source: claude-code-session
tags: [git, worktree, claude-code, recuperacion]
---
El working tree de cada `git worktree` conserva sus cambios sin commitear tras
un apagón — no se pierde nada, solo hay que localizarlo. Triaje:

1. `git worktree list` — cada rama/sesión aislada.
2. Por worktree: `git -C <wt> status -s` (dirty) + `git -C <wt> log origin/main..HEAD`.
3. `find <wt> -mtime -2 -type f` para ver el mtime más reciente → ese era el
   worktree activo al caer (el "¿dónde iba?").
4. `git stash list` + `git reflog` para rescates parciales.

El branch mostrado en el status de arranque puede estar obsoleto si otra sesión
cambió HEAD del dir principal — fía del worktree, no del cwd. Ver
[[auditar-sobre-origin-main-worktree-no-cwd-stale]] y
[[agente-background-en-worktree-build-cuelga-watchdog]].
