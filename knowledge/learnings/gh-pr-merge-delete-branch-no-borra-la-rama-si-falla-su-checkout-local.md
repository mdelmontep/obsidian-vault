---
title: gh pr merge --delete-branch deja la rama viva si falla su checkout local
date: 2026-08-17
updated: 2026-09-20
source: claude-code-session
tags: [git, github, worktrees, gh-cli]
---

> Fusión de tres notas que decían este mismo hecho (20-sep-2026): las del 17-jul y el 29-jul
> se absorbieron aquí con lo que cada una aportaba.

`gh pr merge N --squash --delete-branch` hace **dos cosas**: mergea en el remoto vía API y
luego limpia la rama, y para lo segundo intenta un `git checkout` de la rama base en tu repo.
Si ese checkout falla, el comando sale con error **después de haber mergeado** — el merge ya
es irreversible.

La condición exacta **no es «tener worktrees»**, es que la **rama base esté ocupada** cuando
el comando intenta hacerle checkout:

    failed to run git: fatal: 'main' is already used by worktree at '/Users/…/facturaia'

Se aisló con un **control negativo**, no con repeticiones: tres fallos seguidos en una tarde
solo decían «pasa mucho». El cuarto merge, con el repo local **en la rama del PR** y `main`
libre, salió con EC=0 y **sí borró la rama**. Sin ese caso positivo la nota habría quedado en
«desconfía de este comando» —el síntoma— en vez de «desconfía cuando la base está ocupada»,
que es la causa y se puede comprobar **antes**.

**Segundo disparador, sin worktrees** (21-ago, facturaia): un fichero **untracked** en local
que `main` ya trae **tracked** → `error: The following untracked working tree files would be
overwritten by checkout`. Antes de borrarlo, compara con
`git cat-file -p origin/main:<ruta>`: aquel día la versión de `main` era la nueva (otra sesión
la commiteó) y la local la vieja — al revés habrías perdido trabajo.

El resultado engaña **en las dos direcciones**: la salida parece un fallo (el merge SÍ se
hizo) y la rama que dabas por borrada **sigue viva en el remoto**.

Qué hacer:
- Antes: si `git worktree list` enseña la rama base ocupada, cuenta con borrar a mano.
- Después: `gh pr view N --json state,mergedAt` y `git ls-remote --heads origin | grep <rama>`.
  Ninguna de las dos se deduce del exit code.
- Borra tú, en un paso aparte: `git push origin --delete <rama>` (o
  `gh api -X DELETE repos/<owner>/<repo>/git/refs/heads/<rama>`), y el worktree con
  `git worktree remove <path> --force` + `git branch -D <rama>`.
- Reintentar solo `gh pr merge N --squash` (sin `--delete-branch`) devuelve «already merged».

Es el mismo patrón de [[el-instrumento-devuelve-cero-sin-decir-que-no-ha-medido]]: un comando
compuesto cuyo exit code no dice qué mitad se ejecutó. Caso contrario —el merge **no** se hizo
y lo parece— en [[gh-pr-merge-no-confirma-verificar-state-merged]]. Y el borrado **nunca** va
encadenado al merge: [[el-borrado-de-rama-nunca-va-encadenado-al-merge]] ·
[[triaje-seguro-ramas-worktrees-sesiones-paralelas]]
