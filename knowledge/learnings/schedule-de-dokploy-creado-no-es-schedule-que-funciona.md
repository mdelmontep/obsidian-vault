---
title: un schedule de Dokploy creado no es un schedule que funciona — verifícalo en la BD de la app
date: 2026-08-17
source: claude-code-session
tags: [dokploy, cron, verificacion, gotcha]
---

`schedule.create` devuelve un `scheduleId` y `schedule.runManually` devuelve
`status: done`. Ninguna de las dos cosas dice que el cron HAGA algo: `done` solo significa
que el comando se ejecutó dentro del contenedor. Si el endpoint no existe (deploy por
detrás del merge) o la firma HMAC no valida, el `done` sale igual.

**Verificación real**: la tabla de tracking de la propia app (en TuFacturaIA, `cron_runs`
vía `withCronTracking`) — buscar la fila con `status: success` y `triggered_by: dokploy`.
Eso demuestra el circuito entero: Dokploy → `sign-call.sh` (HMAC) → endpoint → BD.
Comprobar antes que el `deployments[]` del compose lleva un commit que ya incluye el
código, o el cron llamará a un 404.

**Crearlos por la API del panel, nunca con `crontab` en el host**: los schedules viven en
la BD de Dokploy; uno metido a mano queda invisible en el panel y se pierde en la
siguiente migración del stack. Misma razón por la que el compose se edita en el panel.

El momento barato para dispararlos a mano es cuando la tabla que procesan está vacía: se
prueba el circuito sin efectos. Ver [[dokploy-guarda-en-su-bd-y-no-toca-el-disco]].
