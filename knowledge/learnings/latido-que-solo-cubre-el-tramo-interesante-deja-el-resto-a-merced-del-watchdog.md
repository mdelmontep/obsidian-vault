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

Mover el intervalo al inicio del job y cerrarlo en el `finally` es necesario pero **no basta**, y
darlo por arreglado fue el error: en Node un `setInterval` no se dispara mientras el event loop está
bloqueado por trabajo síncrono (`spawnSync`, `cpSync`). Repro: 4019 ms de trabajo síncrono → **0
latidos**, cuando tocaban ~20. O sea que el tramo que motivó el cambio, la copia del GB con `cpSync`,
seguía sin latir. La lección general: un latido por temporizador solo protege los tramos
asíncronos. Un tramo síncrono largo necesita latido explícito intercalado o volverse asíncrono. Si
no, el watchdog mide silencio del loop, no salud del job.
Arreglado de las dos formas a la vez (#1359): `cpSync` → `await cp` de `fs/promises` y `heartbeat()`
intercalado entre los pasos síncronos. Medido: con `cpSync` 0 latidos, con `await cp` 6 de 6.
CUIDADO con dar el síntoma por cerrado. Esa misma noche 3 jobs volvieron a morir como "sin latido",
y la causa era otra: el compose del runner tenía `autoDeploy` contra `main`, así que **cada merge
recreaba su contenedor y cortaba la sesión en marcha**. Comprobado por horas: los jobs perdieron el
latido a las 21:25 y 21:44 UTC, que son los minutos exactos de dos merges míos. Yo lo achaqué a OOM
por memoria y a las réplicas, y era falso.
"Sin latido" NO significa "bug del latido": significa que nadie latió. Antes de tocar el código del
latido, mira quién mató al proceso, y sospecha de tu propio deploy antes que del host.

Y el motivo de que no se viera en las métricas: **el evento de fase se emite DESPUÉS del tramo caro**,
así que "preparando" figuraba con 0,0 min de media. Un tramo cuya duración se mide desde su final
es un tramo sin medir. Al instrumentar por fases, marca el inicio, no el fin.

Ver [[orden-imposible-en-su-entorno-el-agente-explora-hasta-que-lo-matan]] · [[turbopack-rechaza-symlink-node-modules-en-worktree]]
