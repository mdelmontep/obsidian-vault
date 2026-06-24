---
title: agente background en worktree que corre `npm run build` cuelga el watchdog (~600s)
date: 2026-06-19
source: claude-code-session
tags: [claude-code, agentes, workflow, build, facturaia]
---

Al lanzar varios Agent en background con `isolation: worktree` para implementar+verificar+PR en paralelo: si su verificación incluye `npm run build` completo (Next/Turbopack, largo y sin output intermedio), el **stream-watchdog mata al agente por "no progress for 600s"**. El agente reporta `failed` aunque hizo bien el trabajo (típico: lint+typecheck pasaron, murió en el build).

Síntoma: notificación `Agent stalled: no progress for 600s`, último mensaje tipo "now build" / "now run smoke".

Recuperación preferida: **`SendMessage` al `agentId` del agente caído** → reanuda en background desde su transcript, con worktree y contexto intactos, y cierra él mismo (incl. su propio gate). Solo termina tú a mano (`git -C .claude/worktrees/agent-<id>` → build+tests, commit, PR) si el resume no progresa. El stall NO siempre es el build: puede colgarse en lectura/razonamiento por stream, o reportar truncado por error de conexión → **verifica el worktree directamente, no te fíes del reporte final del agente**.

Prevención: en el prompt pide verificar con `lint`+`typecheck`+**unit tests** (no el build completo); deja el build pesado para ti al integrar. Casos: 3 mejoras MCP (#396/#397/#398) colgadas en build; refactor arquitectura #472/#473/#474 (2 muertos en stream, 1 truncado) recuperados con SendMessage. Ver [[claude-code-sesiones-paralelas-mismo-repo-colisiones-git]] · [[claude-code-agentes-worktree-failure-modes]].
