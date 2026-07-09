---
title: retirar un cron deja el scheduler externo huérfano y su 404 no deja rastro
date: 2026-07-09
source: claude-code-session
tags: [dokploy, crons, observabilidad, cutover]
---
Al retirar un endpoint de cron de la app, el scheduler EXTERNO que lo dispara (Dokploy schedule, cron del SO, n8n) sigue vivo golpeando la ruta retirada → 404 cada tick.

Gotcha de observabilidad: ese 404 NO crea fila en `cron_runs` (esa tabla se escribe DENTRO del endpoint, vía `withCronTracking`), así que desde la BD de la app es indistinguible de "scheduler ya borrado", y el watchdog tampoco lo ve si el cron ya salió del registry. Queda invisible.

Regla de cutover: retirar un cron = borrar TAMBIÉN su schedule externo en el mismo paso.

Verificar en Dokploy sin exponer secretos: SSH read-only + `select name, "cronExpression", enabled from schedule` en el contenedor `dokploy-postgres`. NO usar `schedule.one`/`compose.one` (vuelcan el env con secretos, ver [[dokploy-api-get-schedule-list-expone-env-completo-secrets]]); `schedule.all` da 404. Borrar con `schedule.delete {scheduleId}`.

Caso real: cola OCR FacturaIA — `ingesta-stale-sweep` quedó enabled 404-eando cada 30 min tras el deploy #802 que retiró su endpoint. Ver [[cron-health-desconocido-para-cron-sin-ningun-run]].
