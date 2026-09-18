---
title: un push encolado en fia-gate empuja el HEAD del momento en que sale
date: 2026-09-18
source: agh-iberica
tags: [fia-gate, git, harness, gates]
---
`git push` y `gh pr create` pasan por el semáforo [[fia-gate]]. Con gates de otras sesiones en la cola, el push esperó ~20 min sin dar señal de vida: el log conservaba el contenido de un push anterior y `ps` no mostraba ningún `git push`.

**Gotcha:** el push lee `HEAD` cuando consigue el slot, no cuando se lanza. Un commit hecho mientras espera se sube también, y la PR nace con una punta que el gate no midió (AGH #1869: el cuerpo decía 2 ficheros y eran 3).

**Patrón:**
- No commitear en una rama con un push en cola.
- Si ya ocurrió: re-medir sobre la punta final y contar `gh pr diff --name-only` antes de pegar la línea del gate.
- Saber si sigue en cola: `ps -eo pid,etime,command | grep fia-gate`. Esperar con `kill -0 <pid>`, no con `grep` sobre un log que todavía no se ha truncado.
