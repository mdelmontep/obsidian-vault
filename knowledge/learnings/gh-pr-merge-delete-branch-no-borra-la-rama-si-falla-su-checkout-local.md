---
title: gh pr merge --delete-branch deja la rama viva si falla su checkout local
date: 2026-08-17
source: claude-code-session
tags: [git, github, worktrees, gh-cli]
---

`gh pr merge N --squash --delete-branch` hace **dos cosas**: mergea en el remoto y luego
limpia la rama, y para lo segundo intenta un `git checkout` de la rama base en tu repo. Si
ese checkout falla, el comando sale con error **después de haber mergeado**.

La condición exacta **no es «tener worktrees»**, es que la **rama base esté ocupada** por otro
worktree cuando el comando intenta hacerle checkout:

    failed to run git: fatal: 'main' is already used by worktree at '/Users/…/facturaia'

Y el resultado engaña en las dos direcciones: la salida parece un fallo (el merge SÍ se
hizo) y la rama que dabas por borrada **sigue viva en el remoto**.

La condición se aisló con un **control negativo**, no con repeticiones: tres fallos seguidos
en una tarde solo decían «pasa mucho». El cuarto merge, con el repo local **en la rama del
PR** y `main` libre, salió con EC=0 y **sí borró la rama**. Sin ese caso positivo la nota
habría quedado en «desconfía de este comando», que es el síntoma; con él queda en «desconfía
cuando la base está ocupada», que es la causa y se puede comprobar antes.

Qué hacer:
- Antes: si `git worktree list` enseña la rama base ocupada, cuenta con borrar a mano.
- Después: comprueba el estado real con `gh pr view N --json state` y
  `git ls-remote --heads origin | grep <rama>`. No deduzcas ninguna de las dos del exit code.
- Borra tú: `git push origin --delete <rama>`.

Es el mismo patrón de [[el-instrumento-devuelve-cero-sin-decir-que-no-ha-medido]]: un
comando compuesto cuyo exit code no dice qué mitad se ejecutó.
