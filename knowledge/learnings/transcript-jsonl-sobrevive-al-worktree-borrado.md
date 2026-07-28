---
title: el transcript .jsonl sobrevive al worktree borrado — reconstruir la spec, no el código
date: 2026-07-28
source: claude-code-session
tags: [claude-code, git-worktree, recuperacion, sesiones]
---
Un agente trabajó en un worktree bajo `/private/tmp` y devolvió su resultado sin
commitear. El barrido del SO se llevó el directorio: `git worktree list` lo marca
`prunable` y no queda ni un objeto en el repo. El código se perdió entero.

Lo que NO se pierde es el transcript: `~/.claude/projects/<cwd-con-guiones>/<uuid>.jsonl`,
una línea JSON por mensaje, incluidos los `<task-notification>` con el resultado
COMPLETO de cada subagente. Ahí estaba el diseño literal (tipos, severidades,
mensajes de usuario, lista de tests) y reimplementarlo fue mecánico.

Extracción: `python3` leyendo el `.jsonl` y filtrando por palabra clave sobre
`json.dumps(d)`, luego imprimir `message.content` (str, o lista de dicts con
`type: text` / `tool_result`). Grep directo sobre el fichero no basta: el texto
va escapado dentro del JSON.

Corolario para el prompt del agente: exigir commit dentro del worktree ANTES de
devolver, y no usar `/private/tmp` para nada que dure más de unos minutos
(ver failure mode K de [[claude-code-agentes-worktree-failure-modes]]).
`/login` no borra sesiones: `claude --resume` las lista por directorio.
