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
