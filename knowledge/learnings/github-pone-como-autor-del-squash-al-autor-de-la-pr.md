---
title: github pone como autor del squash al autor de la pr, no al de los commits
date: 2026-08-24
source: tecnocloud
tags: [git, github, gh-cli]
---

Repo cuyo `CLAUDE.md` exige que los commits sean de una cuenta concreta (`tecnocloudes`). Los commits
de la rama iban firmados bien (`git -c user.name=… -c user.email=…`), pero el **squash** de
`gh pr merge --squash` entró en `main` con la cuenta que **abrió la PR** — la única autenticada en
`gh` — y la firma correcta se perdió al aplastar.

- El autor del squash **no** se hereda de los commits: sale del autor de la PR.
- Arreglarlo después es reescribir `main` + force push, con el deploy ya lanzado. No se arregla, se
  previene.
- Prevención: abrir la PR con la cuenta que exige el repo, o mergear en local
  (`git merge --squash` + commit con esa identidad + push).
- **Verificar DESPUÉS del merge**, no antes: `git log origin/main -1 --format='%an <%ae>'`. Antes del
  merge todo cuadra y no dice nada.

Corolario: `gh pr merge --delete-branch` puede reportar «failed to run git» por el paso local de
volver a la base (worktree que ya ocupa `main`) **con el merge remoto ya hecho** — comprobar
`origin/main` antes de reintentar, y borrar la rama a mano.
