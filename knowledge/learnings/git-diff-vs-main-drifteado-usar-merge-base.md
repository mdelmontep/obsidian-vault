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
del worktree (diff del commit vs su padre). Inverso real: una rama de worktree creada
sobre un `origin/main` VIEJO, tras rebase, puede arrastrar reverts de ficheros ajenos →
verifica el scope con `git diff --name-only origin/main | grep -v <scope>`, NUNCA con
`git diff --stat | tail -N` (el tail oculta el principio y un commit sucio parece limpio).
Caso real: auditoría 7-PR en paralelo con sesiones de stock/UI mergeando a main a la vez;
y PR de notificaciones que revertía el fix fiscal #494/#503 sin verlo por usar `tail`.
