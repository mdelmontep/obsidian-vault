---
title: execfile falla con "command failed: <comando entero>" y la causa no está en la primera línea
date: 2026-08-13
source: claude-code-session
tags: [node, runners, observabilidad]
---

Cuando `execFile` falla, `e.message` empieza por `Command failed: <binario> <argv completo>`.
Si un argv es multilínea (un prompt de LLM), el patrón habitual `e.message.split('\n')[0]`
devuelve el comando TRUNCADO en el primer salto de línea del prompt: el `last_error`
guarda kilobytes de prompt y cero causa (caso real: run del guionista de TuFacturaIA
fallido el 13-ago, indiagnosticable desde el panel).

La causa vive en las propiedades, no en el mensaje:
- `e.code` numérico = exit code · string (`ENOENT`…) = fallo de spawn
- `e.killed` + `e.signal` = timeout de `execFile` o kill externo
- `e.stderr` = lo que dijo el binario (adjuntar recortado)

Fix en TuFacturaIA: `describirErrorExec` en `services/marketing-runner/claude-headless.mjs` (PR #1723).
