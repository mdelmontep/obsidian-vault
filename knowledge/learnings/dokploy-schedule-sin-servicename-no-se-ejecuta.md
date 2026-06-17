---
title: un schedule "compose" de Dokploy sin serviceName (o scheduleType=application) no se ejecuta nunca
date: 2026-06-17
source: claude-code-session
tags: [dokploy, crons, infra]
---

Un schedule de Dokploy sobre un stack compose necesita `scheduleType:'compose'`
+ `serviceName:'<servicio>'` para saber en qué contenedor hacer `exec` del
comando. Si se crea (por API o UI) como `scheduleType:'application'` o sin
`serviceName`, queda **enabled pero NO dispara nunca** — silencioso. Al
ejecutarlo a mano (`schedule.runManually`) da `invalid container name or ID:
value is empty`.

Caso TuFacturaIA: 3 crons rotos así (`fiscal-generar-borradores` 06-10,
`stock-alarmas-email` 06-15, y `suspend-overdue` directamente sin schedule) —
"enabled" en el panel pero sin filas en `cron_runs`. Algo los daba de alta mal.

Fix: recrear con `schedule.create` `{scheduleType:'compose', serviceName:
'facturaia', composeId, shellType:'bash', command:'sh /app/ops/cron/sign-call.sh
/api/internal/<endpoint> POST'}` y borrar el corrupto. **Al crear cualquier cron
nuevo por API, pasar SIEMPRE `scheduleType:'compose'` + `serviceName`.** El
`schedule.update` además es finicky (puede flipar `scheduleType`): mejor
delete+create. Ver [[monitor-en-la-misma-infra-no-detecta-su-propia-muerte]].
