---
title: un timer más largo que la cadencia de despliegue no corre nunca
date: 2026-08-06
source: claude-code-session
tags: [dokploy, deploy, worker, scheduling, agh-iberica]
---

Un `setInterval(24h)` en un servicio con autodeploy **no dispara jamás** si se mergea más de una vez
al día: cada redespliegue recrea el contenedor y el contador vuelve a cero.

Caso AGH (06-ago, #953): el barrido de hilos abiertos llevaba 4 días sin correr. La prueba no fue
leer el código sino la BD — ante un fallo el job reprograma el reintento a `now`, así que las filas
estaban vencidas desde hacía 4 días y **el timestamp que el propio job escribe no se había movido**.
`start()` solo armaba el `setInterval`, sin pasada inicial. Ese día: 5 arranques en una hora.

**El control que zanja el debate «cola vs polling»:** en el MISMO proceso y con la MISMA cadencia de
despliegues, los recordatorios sí entregaban (16 en un mes). La diferencia no era BullMQ contra
`setInterval`: era que `reminders` reconcilia desde Postgres **síncronamente en el arranque** y el
otro no. Cambiar de librería no lo habría arreglado.

- Todo worker periódico: **una pasada síncrona en el boot** antes de armar el timer.
- Olfato: si el intervalo > cadencia de despliegue, el timer es decorativo.
- Todo job de fondo necesita un **heartbeat consultable** (`last_swept_at`): sin él no se puede echar
  en falta lo que no pasa. Y ojo — «resiliente a reinicios» suele predicarse del DATO y creerse del
  MECANISMO; el dato duraba, el barrido no.

Ver [[autodeploy-sin-watchpaths-mata-el-trabajo-en-vuelo-del-worker]] · [[persistir-el-error-no-basta-si-ninguna-superficie-lo-lee]]
