---
title: un latido que solo cubre el tramo interesante deja el resto del job a merced del watchdog
date: 2026-07-29
source: claude-code-session
tags: [runner, watchdog, observabilidad, facturaia]
---

Seis jobs del runner de tickets murieron como "runner sin latido > 15 min" **estando sanos**. El
`setInterval` del heartbeat vivía dentro de la función que ejecuta al agente, así que todo lo de
antes corría a oscuras: `git fetch`, `worktree add` y sobre todo la copia de `node_modules` (copia
real de más de un GB de ficheros pequeños; no puede ser hardlink porque el symlink rompe Turbopack).

El latido es del **job**, no de la parte llamativa del job: abrir el intervalo al entrar y cerrarlo
en el `finally`. Si aparece un `await heartbeat()` suelto antes de una fase lenta, eso es el síntoma
de que el intervalo está mal colocado, no la solución.

Y el motivo de que no se viera en las métricas: **el evento de fase se emite DESPUÉS del tramo caro**,
así que "preparando" figuraba con 0,0 min de media. Un tramo cuya duración se mide desde su final
es un tramo sin medir. Al instrumentar por fases, marca el inicio, no el fin.

Ver [[orden-imposible-en-su-entorno-el-agente-explora-hasta-que-lo-matan]] · [[turbopack-rechaza-symlink-node-modules-en-worktree]]
