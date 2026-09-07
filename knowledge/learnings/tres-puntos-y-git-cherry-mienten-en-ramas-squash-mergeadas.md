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

**Reincidencia 18-ago, con esta nota ya escrita.** En la limpieza del home caí tres
veces seguidas: di `agentesia-web` por «26 commits en riesgo de perderse» cuando
llevaban 11 días en `main` (PR #99), lo repetí con otras 31 ramas de facturaia, y
solo lo vi al fallar un `git push` con 403. La nota no falló; falló consultarla —
vive en el vault y no se carga sola. Antes de triar ramas o worktrees:
`vault-find "squash cherry ramas"`. Un learning sin consultar es un learning que no
existe.

**Tercera reincidencia, 5-sep, en OTRO contexto: censar números de migración.** Para
avisar a otra sesión de qué huecos estaban cogidos enumeré ramas con
`git diff --name-only origin/main...<rama> -- supabase/migrations/` y le pasé cuatro
como reservas vivas. Tres eran fantasmas: 840-842, 844-846 y 793-795 ya estaban en
`main` con esos mismos nombres. El mismo fallo de tres puntos, pero disfrazado —
aquí no triaba ramas, contaba números, así que la nota no me vino a la cabeza. **La
comprobación correcta no era comparar árboles, era mirar el número en `main`
directamente** (`git ls-tree origin/main supabase/migrations/ | grep '^NNN_'`), que
además distingue lo único que importa: mismo número con OTRO contenido (colisión
real) de mismo número con el mismo (ya mergeado). Regla: cuando la pregunta es «¿este
identificador está ocupado?», se mira el identificador en el destino, nunca el diff
de quien lo propone.
