---
title: git worktree prune da OK y no recoge nada — el problema es invisible por diseño
date: 2026-09-11
source: agency-portal
tags: [git, worktrees, disco, arnes]
---
Medido: 90 worktrees en un repo, 88 con `node_modules` propio, el más viejo de dos semanas.
`git worktree prune` devuelve OK y recoge **cero**.

No es un bug: `prune` solo borra registros cuyo DIRECTORIO ya no existe. Un worktree abandonado
por una sesión muerta sigue con su directorio en disco, así que para git está perfectamente vivo.
El comando que todo el mundo corre para limpiar es exactamente el que no ve el problema.

Para verlos hay que mirar antigüedad, no registros:
```bash
git worktree list --porcelain | awk '/^worktree /{print $2}' \
  | while read d; do [ -d "$d" ] && printf '%s %s\n' "$(stat -f %m "$d")" "$d"; done | sort -n
```
Y desde fuera del repo no se ven: `git worktree list` hay que correrlo dentro.

Ojo al diagnosticar memoria: son bytes en DISCO, RSS cero. No explican un OOM.
