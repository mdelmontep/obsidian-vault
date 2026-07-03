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

**El cierre en cascada NO es exclusivo de squash**: mergear la base con `--merge` normal (commit de merge, sin squash) y borrar su rama TAMBIÉN cierra la PR stacked cuya `base` apuntaba a esa rama — GitHub cierra cualquier PR cuya base branch desaparece, sin distinguir el tipo de merge. Caso real 2026-07-03 (facturaia, stack de 5 PRs #668→#669→#672→#674→#677): al mergear #668 (`--merge`) y borrar su rama, #669 se cerró en vez de retargetarse. **Alternativa más rápida que rebasear cada PR de la cadena una a una**: si la PUNTA de la pila ya contiene todos los commits acumulados (habitual en cadenas WS1→WS2→WS3...), en vez de repetir el rebase/reapertura por cada PR intermedio, fusiona `main` DIRECTAMENTE en la rama de la punta (`git merge origin/main`), resuelve los conflictos UNA sola vez, y mergea esa única rama contra `main` (`gh pr edit <punta> --base main` + merge). Las PRs intermedias quedan `CLOSED` (o `MERGED` automático si sus commits ya están en main) sin pérdida de contenido — más rápido que rebasear N veces cuando N≥3. Precaución: probar el merge de prueba en un worktree DESECHABLE (`git worktree add --detach /tmp/...`), nunca en el worktree que tiene la rama de trabajo real activa (`git checkout --detach` ahí deja el working tree en conflicto sin commitear).

Relacionado: [[audits-cross-pr-vs-per-pr]].
