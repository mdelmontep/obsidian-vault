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

**PRs APILADAS con squash**: mergear la base con `--delete-branch` **cierra en cascada** la PR stacked (su base branch desaparece) y GitHub **no la deja reabrir ni retargetear**. Orden correcto: mergear la base SIN `--delete-branch` → `git rebase --onto origin/main <base-sha> <stacked>` (replaya solo los commits propios; el squash de la base no comparte SHA) → force-push → `gh pr edit <stacked> --base main` → mergear → limpiar ramas al final. Caso real: #550 se cerró al borrar #544; hubo que recrearla como #552.

**El gotcha de "apiladas" NO es exclusivo de squash**: `git rebase <rama-base>` a secas (sin `--onto`) sobre una rama-base creada de un `main` más viejo que el actual replaya TODO lo que main avanzó entre medias como commits nuevos con SHAs distintos dentro de tu rama — aunque nunca hubiera squash de por medio. Caso real 2026-07-01: al apilar el PR de fix de tests sobre el PR de fix de CI (éste basado en un main previo a que se mergeara una cadena de 7 features), la rama de tests terminó "duplicando" esa cadena entera con SHAs nuevos, ensuciando el diff de 6 a 34 archivos. Regla general, con o sin squash: usar siempre `git rebase --onto origin/main <base-sha> <stacked>` (o, más simple si no hay conflictos, reconstruir con `git checkout -b <rama> origin/main` + `git cherry-pick <mis-commits>`), nunca `git rebase <rama-base>` a secas.

Relacionado: [[audits-cross-pr-vs-per-pr]].
