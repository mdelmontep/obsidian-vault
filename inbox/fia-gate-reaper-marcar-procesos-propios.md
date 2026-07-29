---
title: arreglar el reaper de fia-gate para que no mate jobs de otras sesiones
date: 2026-07-29
source: claude-code-session
tags: [claude-code, harness, fia-gate]
---

`reap_orphans()` mata por "PPID 1 = huérfano", y un `run_in_background` del harness cumple esa
condición estando vivo → mata typecheck/build de otras sesiones. Costó 4 relanzamientos en el gate
de #1326/#1327 (29-jul).

Arreglo propuesto: que `fia-gate` exporte una marca en el entorno de sus hijos (p. ej.
`FIA_GATE_JOB=<id>`) y `reap_orphans` solo mate procesos **sin** esa marca — o que compruebe el
`.pid` de los slots vivos antes de matar. Mientras tanto, workaround: invocar por la ruta real
(`node ./node_modules/typescript/bin/tsc`), que no casa el patrón.

Ver [[fia-gate-reap-orphans-mata-jobs-de-otras-sesiones]] · [[fia-gate]]
