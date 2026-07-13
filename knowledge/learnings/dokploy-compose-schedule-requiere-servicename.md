---
title: schedule Dokploy tipo compose exige serviceName — sin él runManually 500 y el cron no dispara
date: 2026-07-13
source: claude-code-session
tags: [dokploy, cron, infra]
---
Al crear un schedule Dokploy `scheduleType: compose` vía API, si falta `serviceName`
(el servicio del compose, p.ej. `facturaia`) el job no resuelve el contenedor:
`runManually` → **500 "invalid container name or ID: value is empty"**, y el cron
programado tampoco ejecuta → 0 filas en `cron_runs` → invisible. Copiar de un cron que
funciona los campos exactos: `serviceName` + `shellType: 'bash'`. Fijar `timezone` en el
**CREATE**, no por `update` (el update cambia la fila pero no re-registra el trigger vivo,
seguía en UTC → disparaba a las 08:00 UTC en vez de 08:00 Madrid).

**Blind spot de monitorización**: un cron que NUNCA ha corrido = `desconocido` para el
watchdog → NO alerta (solo alerta los que ya corrieron y se quedan stale). Al añadir un
cron nuevo, verifica el PRIMER run a mano (`runManually` → `cron_runs` success), no asumas.
Ver [[pr-apilado-squash-cierra-al-borrar-base]].
