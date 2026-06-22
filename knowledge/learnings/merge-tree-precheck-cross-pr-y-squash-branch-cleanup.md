---
title: verificar conflicto cross-PR con merge-tree antes de mergear; squash rompe branch --merged
date: 2026-06-22
source: claude-code-session
tags: [git, pr, workflow, gotcha]
---
**Dos PRs que tocan el mismo archivo**: no asumir "no debería conflictuar" — verificarlo SIN checkout con:

`git merge-tree --write-tree --merge-base <base> <ramaA> <ramaB>`

Sale exit≠0 + `CONFLICT (content): ... <archivo>` si chocan. Caso real: #444 añadía `<X/>` justo tras un bloque que #448 borraba → conflicto que negué "de memoria" y sí existía. Resolución correcta verificada compilando (trial-merge en branch temporal + lint/typecheck) antes de mergear, y documentada en ambos PRs para quien mergee segundo.

**Limpieza tras squash-merge**: el squash crea un commit nuevo cuyos padres NO incluyen la rama → `git branch --merged origin/main` NO la lista. Borrar con `git branch -D` (no `-d`, que se niega) + `git push origin --delete`, tras confirmar que el contenido está en main.

Relacionado: [[audits-cross-pr-vs-per-pr]].
