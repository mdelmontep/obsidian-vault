---
title: gh pr merge --delete-branch puede fallar en local aunque el merge en GitHub ya se hizo
date: 2026-07-17
source: claude-code-session
tags: [github, gh-cli, git-worktree, gotcha]
---

`gh pr merge <n> --squash --delete-branch` en un repo con varios `git worktree` activos puede
devolver exit code 1 con `fatal: 'main' is already used by worktree at '<path>'` — pero el
PR YA SE MERGEÓ en GitHub antes de ese paso. El comando hace el squash-merge remoto primero y
solo DESPUÉS intenta `git checkout main` local para poder borrar la rama; si `main` está
checked out en OTRO worktree, ese segundo paso peta, pero el merge real ya es irreversible.

El error engañó: parecía que el merge había fallado. Verificación real:
`gh pr view <n> --json state,mergedAt` → `state=MERGED`.

Fix: reintentar solo `gh pr merge <n> --squash` (sin `--delete-branch`) → devuelve
"already merged"; borrar la rama remota aparte con
`gh api -X DELETE repos/<owner>/<repo>/git/refs/heads/<rama>` y el worktree local con
`git worktree remove <path> --force` + `git branch -D <rama>`.

Mismo principio que [[gh-pr-merge-no-confirma-verificar-state-merged]]: nunca fiarse del
exit code/stdout de `gh pr merge`, verificar siempre `state=MERGED`.
