---
title: gh pr merge --delete-branch deja la rama viva si falla su checkout local
date: 2026-08-17
source: claude-code-session
tags: [git, github, worktrees, gh-cli]
---

`gh pr merge N --squash --delete-branch` hace **dos cosas**: mergea en el remoto y luego
limpia la rama, y para lo segundo intenta un `git checkout` de la rama base en tu repo. Si
ese checkout falla, el comando sale con error **después de haber mergeado**.

Con worktrees siempre falla:

    failed to run git: fatal: 'main' is already used by worktree at '/Users/…/facturaia'

Y el resultado engaña en las dos direcciones: la salida parece un fallo (el merge SÍ se
hizo) y la rama que dabas por borrada **sigue viva en el remoto**. Lo descubrí al revisar
cabos al final de la sesión, no en el momento.

Qué hacer:
- Tras un merge que falle así, comprueba el estado real: `gh pr view N --json state` y
  `git ls-remote --heads origin | grep <rama>`. No deduzcas ninguna de las dos del exit code.
- Borra tú: `git push origin --delete <rama>`.
- Si el PR lo abres desde un worktree, `--delete-branch` no te sirve de nada: cuenta con
  hacerlo a mano.

Es el mismo patrón de [[el-instrumento-devuelve-cero-sin-decir-que-no-ha-medido]]: un
comando compuesto cuyo exit code no dice qué mitad se ejecutó.
