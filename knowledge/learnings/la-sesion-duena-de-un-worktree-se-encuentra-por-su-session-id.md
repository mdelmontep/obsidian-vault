---
title: la sesión dueña de un worktree se encuentra por su session id, no por el nombre
date: 2026-09-24
source: facturaia
tags: [claude-code, cross-session, fia-gate, coordinacion]
---
`ListAgents` lista nombres (`facturaia-2a`) sin el cwd ni la rama, y el cwd de los procesos `claude` suele ser el checkout principal aunque la sesión trabaje en un worktree. Así que «¿quién tiene aplicada esta migración en la base compartida?» no se contesta mirando procesos.

Lo que sí funciona (24-sep, ticket 182 contra la pila `paquetes-*`):
1. `grep '<worktree o rama>' ~/.claude/gate/state/events.jsonl | grep -o '"session":"[^"]*"' | sort | uniq -c`: los gates que corrió cada sesión, con su UUID.
2. `grep -l <uuid> ~/.claude/sessions/*.json`: el `name` de ese fichero es la dirección de `SendMessage`.

Con eso se coordina el turno de un recurso compartido (la base local `fia-dbtest`) en vez de pisarlo. Y un recurso compartido no se «restaura a su estado original» sin leer ese estado justo antes: yo reactivé un trigger que otra sesión había desactivado. Ver [[claude-code-gotchas]].
