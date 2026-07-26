---
title: un monitor que corre en la misma infra que vigila no detecta que esa infra muera
date: 2026-06-17
source: claude-code-session
tags: [monitorizacion, crons, dokploy, observabilidad]
---

Un health-check/sweep que corre COMO un cron del mismo scheduler que vigila
tiene un punto ciego fatal: si el scheduler (o el host) muere, el propio
monitor muere con él y no puede avisar.

Caso TuFacturaIA 2026-06-17: `system-health-sweep` (cron Dokploy que emaila
crons caídos) no avisó de un blackout de ~7-9h del control-plane de Dokploy
(OOM del host sin swap) porque era un cron más → cayó con el resto. Silencio
total durante horas.

Fix: **dead-man's-switch EXTERNO** en infra independiente. Un servicio fuera
(GitHub Action, healthchecks.io, UptimeRobot) consulta un endpoint de salud
o espera pings periódicos y **avisa cuando dejan de llegar**. La app
(data-plane) suele sobrevivir a la caída del control-plane, así que puede
servir el endpoint y reportar "scheduler muerto". Regla: el watchdog de una
infra NUNCA debe vivir dentro de esa infra.

Implementación TuFacturaIA 2026-06-22: NotCaído heartbeat (ID 34) +
`pingSchedulerHeartbeat()` en `withCronTracking` (PR #447) → `NOTCAIDO_HEARTBEAT_URL`
env Dokploy → ntfy topic `notcaido-mdm-PN7YzRN3iIA` si silencio >2 min.

## 2026-07-26: implementado ≠ verificado

La app estuvo caída (`app.tufacturaia.com` → 404 de Traefik) porque la instancia
de Postgres se quedó sin CPU y el contenedor dejó de pasar el health check.
El dead-man's-switch de arriba DEBÍA cubrir exactamente esto: `webhook-dispatcher`
y `drive-sync-dispatcher` corren cada minuto y pingean NotCaído en cada run, así
que con la app en 404 el silencio salta a los 2 minutos.

No llegó ningún aviso: el dueño se enteró porque había una sesión de trabajo
abierta mirando. O `NOTCAIDO_HEARTBEAT_URL` ya no está en el entorno de Dokploy, o
el monitor está pausado, o la notificación no alcanza el móvil.

Regla que faltaba: **un dead-man's-switch escrito no es un dead-man's-switch
verificado.** Hay que probarlo a propósito —silenciar los pings y comprobar que la
alerta LLEGA— y repetirlo cada cierto tiempo, porque una env que desaparece en un
redeploy lo desactiva sin que nada falle de forma visible. Un vigilante que no se
ha disparado nunca es indistinguible de uno roto.
