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

⚠️ **`git cherry` TAMPOCO sirve, y es el sustituto que uno elige** (medido 15-ago, AGH): compara por
**patch-id**, y un squash colapsa N commits en **uno** con patch-id distinto de todos ellos, así que la
rama entera sale marcada `+`. Sobre 17 worktrees recién mergeados dio **6, 5, 2 y 4 «commits sin
mergear»** estando todos dentro. En un flujo squash su resultado ≠ 0 **no significa nada**; solo vale
en su dirección barata (0 = nada que rescatar, fin).

Limpieza segura de worktrees:
- `git worktree prune` → solo quita bookkeeping de dirs ya borrados (100% seguro).
- El resto: verificación rama a rama (¿pusheada a origin? ¿su PR/issue cerrado?) ANTES de borrar.
- Si hace falta comparar CONTENIDO, acótalo a **los ficheros de la rama**, o el diff sale enorme y es
  `main` yendo por delante, no la rama guardando algo:
  `git diff origin/main <rama> -- $(git diff --name-only $(git merge-base origin/main <rama>) <rama>)`
  → `0 líneas` en las 17.

**Cuarta caída, 9-sep (facturaia, cierre del ticket 169).** Al barrer 18 ramas `tk169` volví a
lanzar `--is-ancestor`: las 18 salieron «pendientes» y estuve a un paso de reportarlas como trabajo
sin mergear. La nota existía desde julio; no la consulté.

**En un flujo GitHub squash el test barato no es comparar árboles, es preguntar por el PR:**
```bash
gh pr list --head "<rama>" --state all --json number,state -q '.[] | "\(.number) \(.state)"'
```
`MERGED` cierra la pregunta en una llamada, sin merge-base ni diffs, y de paso te da el número de PR
para el registro. Las 18 dieron MERGED. Reserva la comparación de árboles para ramas **sin PR**.
Antes de borrar, deja los SHA en un fichero: el borrado es recuperable si sabes a qué volver.

**Quinta caída, 12-sep (facturaia, barrido de 23 ramas `feat/marketing-*`).** Volví a medir con
`--is-ancestor` y salieron **las 23 «sin mergear»**; 15 lo estaban. Para un BARRIDO el `gh pr list
--head` de arriba son N llamadas: con **una** basta, cruzando por nombre de rama.
```bash
gh pr list --state merged --limit 900 --json headRefName -q '.[].headRefName' | sort -u > /tmp/mrg
git for-each-ref --format='%(refname:short)' refs/heads | grep -vxF -f /tmp/mrg   # las huérfanas de verdad
```
Y el diff de árbol contra `main` **no** es el desempate de las que sobran: las 7 huérfanas reales
daban −17.000/−24.000 líneas, que es `main` yendo por delante, no trabajo suyo.
