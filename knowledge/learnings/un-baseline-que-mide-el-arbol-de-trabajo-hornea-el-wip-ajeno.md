---
title: un baseline que mide el árbol de trabajo hornea el WIP de otra sesión
date: 2026-08-18
source: obsidian-vault
tags: [gates, repos-compartidos, obsidian]
---
Un trinquete que compara «tamaño actual vs baseline» leyendo el fichero **en disco**
(`readFileSync`) y no el blob de `HEAD` es correcto con una sesión y falso con dos. En un repo que
varias sesiones comparten sin worktree propio, quien corra `--write` mientras otra tiene cambios sin
commitear **acepta como baseline el trabajo ajeno**, y desde entonces el trinquete mide contra una
cifra que no corresponde a ningún commit.

Cómo se detecta: el baseline no cuadra con ningún blob de la historia.
`git cat-file -s HEAD:<fichero>` da 21.065 y el baseline guardado 22.570 → 1.505 bytes de WIP
horneados (caso real en `scripts/context-budget.mjs` del vault, 18-ago).

- Fix de fondo: medir `git show HEAD:<fichero>`, no el árbol.
- Mientras no esté: **no consolidar con el árbol sucio**, y comprobar de quién es lo sucio antes
  (`git log --since` por fichero, no el último commit que lo tocó).

Ver [[stash-es-compartido-entre-worktrees-y-rompe-sesiones-paralelas]].
