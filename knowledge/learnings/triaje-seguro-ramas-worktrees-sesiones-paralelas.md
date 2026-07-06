---
title: triaje seguro de ramas y worktrees con sesiones paralelas
date: 2026-06-12
source: claude-code-session
tags: [git, worktrees, housekeeping, agentes-paralelos]
---

Rama es borrable si **cualquiera** de estas da vacío (evidencia, no fecha):
- `git cherry origin/main rama | grep '^+'` → 0 (patch-equivalente, detecta squash-merge)
- `git diff origin/main rama -- <paths que toca>` vacío (contenido mergeado por otra vía aunque cherry marque `+`)

Worktree con lock: leer el PID del mensaje de error y `ps -p <pid>` — si está muerto, el lock es huérfano y `git worktree remove -f -f` es seguro. Nunca forzar con PID vivo (sesión/agente activo).

Gotcha: un hook pre-push que corre `build` bloquea **hasta los `push --delete` de ramas** si hay un build paralelo (lock `.next/lock`). Ahí `--no-verify` está justificado (el build es irrelevante para borrar una ref).

Rescate si una paralela hizo `git stash` (con nombre) + checkout a otra rama: tus cambios a ficheros **tracked** están en el stash; tus ficheros **nuevos untracked** siguen en el working tree. Sin tocarla: `git worktree add <dir> <tu-rama>` → `git stash apply stash@{N}` → copia los untracked nuevos al worktree → `npm install` (NO symlink, [[turbopack-rechaza-symlink-node-modules-en-worktree]]). Commit ajeno en tu rama: `reset --mixed <tip-bueno>` + `checkout <tip> -- <sus ficheros>` (su commit sigue vivo en su rama).

Regla 2 semanas: lo retomable → pointer en hub antes de borrar; lo demás se va.

**Worktree ajeno con commits propios, aunque verifiques que los ficheros a tocar están intactos** (2026-07-06): el clasificador de seguridad de Claude Code bloquea `cp`/escritura ahí sin confirmación explícita del usuario — "verificado con git diff" no basta como justificación. Si el usuario no responde a tiempo, no forzar: rama/PR separado que referencie el original en la descripción es la salida segura y reversible (fusionar después si se quiere consolidar).
