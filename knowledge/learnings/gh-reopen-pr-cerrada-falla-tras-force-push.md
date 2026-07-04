---
title: reabrir una pr cerrada falla si force-pusheas antes de reabrirla
date: 2026-07-05
source: claude-code-session
tags: [git, github, gh-cli, pr]
---
Una PR cerrada solo se reabre si su rama **aún contiene el head que GitHub tenía registrado**. Si haces `git push --force-with-lease` (p. ej. tras un rebase) *antes* de reabrir, ese commit deja de estar en la rama y `gh pr reopen` falla con `GraphQL: Could not open the pull request (reopenPullRequest)`. No es permisos ni estado merged: es que GitHub no puede reconciliar el head.

**Orden correcto** cuando rebaseas una rama de una PR que está cerrada:
1. `gh pr reopen N` PRIMERO (mientras la PR aún apunta a un commit vivo en la rama).
2. Luego `git push --force-with-lease` → la PR se actualiza al nuevo head y sigue abierta.

Si ya pusheaste y quedó bloqueada: o la reabre el owner desde la web (mismo límite puede aplicar), o abres PR nueva desde la misma rama. Caso real: AGH #136, cerrada por accidente por otra sesión; force-push del rebase la dejó irrecuperable por API. Ver [[gh-borrar-base-de-pr-apilada-cierra-la-hija-irreversible]] · [[claude-code-sesiones-paralelas-mismo-repo-colisiones-git]].
