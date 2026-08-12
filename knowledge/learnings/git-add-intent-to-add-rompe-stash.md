---
title: git add -N (intent-to-add) rompe git stash push/pop
date: 2026-08-12
source: claude-code-session
tags: [git, worktree, stash]
---

`git add -N .` es el truco para que los ficheros nuevos salgan en `git diff`
(útil para pasar un diff completo a un reviewer sin commitear). Pero deja el
index en un estado que `git stash` no sabe manejar: `stash push` falla o deja
a medias con `Entry '<fichero>' not uptodate. Cannot merge`, y el `pop`
posterior suelta `could not restore untracked files from stash`. Dos veces en
la misma sesión (12-ago, facturaia), la segunda a punto de perder 30 ficheros.

Fix: `git reset` (quita el intent-to-add, los ficheros quedan untracked
normales) ANTES de cualquier stash — o directamente commitear y rebasar el
commit, que era lo correcto en ambos casos. El árbol no se pierde: verificar
con `git status --short` + grep de un cambio propio antes de seguir.
