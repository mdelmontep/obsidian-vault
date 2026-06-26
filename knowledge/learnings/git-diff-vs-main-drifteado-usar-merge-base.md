---
title: git diff contra main local drifteado muestra cambios fantasma; usar merge-base
date: 2026-06-26
source: claude-code-session
tags: [git, worktrees, multi-sesion]
---
En trabajo multi-sesión / multi-worktree, otra sesión puede mergear a `origin/main`
y dejar tu `main` local por delante de la base de tus ramas. Entonces
`git diff main <branch>` compara árboles completos y muestra los cambios de la OTRA
sesión como si fueran (al revés) del branch → falsa alarma de "contaminación de scope".
Fix: mira los cambios PROPIOS del branch con
`git diff $(git merge-base main <branch>) <branch>`, o `git show --stat HEAD` dentro
del worktree (diff del commit vs su padre). El commit suele estar limpio aunque el
diff-vs-main parezca sucio. Caso real: auditoría 7-PR en paralelo con sesiones de
stock/UI mergeando a main a la vez; perdí tiempo investigando "stock files" en PRs
fiscales que en realidad eran #504/#496 de otra sesión.
