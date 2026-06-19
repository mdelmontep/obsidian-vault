---
title: agente background en worktree que corre `npm run build` cuelga el watchdog (~600s)
date: 2026-06-19
source: claude-code-session
tags: [claude-code, agentes, workflow, build, facturaia]
---

Al lanzar varios Agent en background con `isolation: worktree` para implementar+verificar+PR en paralelo: si su verificación incluye `npm run build` completo (Next/Turbopack, largo y sin output intermedio), el **stream-watchdog mata al agente por "no progress for 600s"**. El agente reporta `failed` aunque hizo bien el trabajo (típico: lint+typecheck pasaron, murió en el build).

Síntoma: notificación `Agent stalled: no progress for 600s`, último mensaje tipo "now build" / "now run smoke".

Recuperación (el trabajo NO se pierde):
1. `git worktree list` → localizar el worktree del agente (`.claude/worktrees/agent-<id>`) y su rama.
2. `git -C <wt> status` → sus cambios siguen ahí sin commitear.
3. Termina tú: `npm run build` + tests, `git add` explícito, commit, push, PR.

Prevención: en el prompt del agente, pide verificar con `lint`+`typecheck`+**unit tests** (no el build completo) o trocear; deja el build pesado para ti al recuperar. Caso: 3 mejoras MCP (#396/#397/#398) — los 3 se colgaron en el build, recuperados desde sus worktrees. Ver [[claude-code-sesiones-paralelas-mismo-repo-colisiones-git]].
