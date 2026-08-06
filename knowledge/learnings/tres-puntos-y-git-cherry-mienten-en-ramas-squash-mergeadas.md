---
title: git diff de tres puntos y git cherry mienten sobre ramas ya squash-mergeadas
date: 2026-08-06
source: claude-code-session facturaia
tags: [git, worktree, cleanup, squash]
---

Al triar ~90 ramas huérfanas, dos métodos "rápidos" dieron falsos positivos en
direcciones distintas — los dos por la misma causa: ninguno compara el árbol
ACTUAL de la rama contra el árbol ACTUAL de `origin/main`.

- **`git cherry origin/main <rama>`** (patch-id por commit) marcó 37 de 85 ramas
  como "con commits nuevos" cuando estaban 100% ya mergeadas. Un squash combina
  N commits en 1; ningún commit individual de la rama tiene el mismo patch-id
  que el commit combinado, así que TODOS salen `+` aunque el contenido esté.
- **`git diff --stat origin/main...<rama>`** (tres puntos: diff contra el
  merge-base, no contra `origin/main` HOY) mostró diffs de miles de líneas en
  ramas ya squash-mergeadas hace horas — incluida una propia. Mide la
  contribución HISTÓRICA de la rama, no si sobrevive en main.

**El único test fiable:**
```bash
mb=$(git merge-base origin/main <rama>)
files=$(git diff --name-only "$mb" <rama>)
git diff origin/main <rama> -- $files    # vacío = 100% redundante, seguro de borrar
```
Compara los DOS ÁRBOLES ACTUALES, solo en los ficheros que la rama tocó — inmune
a cómo se mergeó (fast-forward, rebase o squash) y a cuánto ha avanzado main desde
entonces.

Con el método correcto, 85/85 ramas confirmadas redundantes de verdad (incluidas
3 que resultaron ser BORRADORES ANTERIORES de un informe que main ya tiene
completo — mergearlas habría sido un retroceso, no una recuperación).

Complementa [[git-merge-base-is-ancestor-falso-negativo-con-squash]] (mismo
problema con `--is-ancestor`) y [[git-diff-vs-main-drifteado-usar-merge-base]]
(dos puntos con `main` drifteado). Los tres apuntan a la misma regla: para
squash-merge, solo vale comparar árboles actuales, nunca commits ni ancestría.
