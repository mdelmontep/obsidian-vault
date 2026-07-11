---
title: git merge-base --is-ancestor da falso negativo con ramas squash-merged
date: 2026-07-11
source: claude-code-session
tags: [git, worktree, cleanup]
---
`git merge-base --is-ancestor <rama> origin/main` devuelve **false** para ramas mergeadas por
SQUASH: el squash crea un commit nuevo en main, así que los commits de la rama NO son ancestros
de main aunque el trabajo SÍ esté integrado.

Consecuencia: no sirve para decidir "¿está esta rama en main?" → **no borres worktrees ni ramas en
bloque basándote en él**. Marcaría como "no mergeado" trabajo que sí está (falso negativo) y podrías
o bien no limpiarlo, o —peor— si inviertes la lógica, borrar trabajo real sin subir.

Limpieza segura de worktrees:
- `git worktree prune` → solo quita bookkeeping de dirs ya borrados (100% seguro).
- El resto: verificación rama a rama (¿pusheada a origin? ¿su PR/issue cerrado?) ANTES de borrar.
