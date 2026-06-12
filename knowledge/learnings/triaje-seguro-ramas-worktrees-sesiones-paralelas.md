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

Regla 2 semanas: lo retomable → pointer en hub antes de borrar; lo demás se va.
