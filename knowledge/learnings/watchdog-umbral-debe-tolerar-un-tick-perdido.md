---
title: umbral de watchdog de cron debe tolerar ≥1 tick perdido (2× intervalo)
date: 2026-06-19
source: claude-code-session
tags: [monitoring, cron, dokploy, facturaia]
---
Un watchdog que marca "cron caído" si el último run supera ~1× su intervalo
da FALSO POSITIVO en cuanto el scheduler se salta un solo tick — algo normal
en deploys o jitter de host. Si el cron está programado en `:30` y el
scheduler pierde ese tick, su siguiente run es 1 intervalo después → el hueco
duplica el intervalo y cruza el umbral.
Regla: `max_intervalo` = 2 × intervalo + buffer. Así un tick perdido nunca
alarma; solo salta ante ≥2 fallos consecutivos (parada real).
Caso TuFacturaIA 2026-06-19: 3 emails ALTA "Cron en fallo" falsos (bot-error
-backfill, ingesta/email zombie-sweep) con todos los runs `success`; el
scheduler de Dokploy perdió el tick 02:30 UTC. Fix #393 (registry.ts).
El `scheduler-heartbeat` ya aplicaba este principio (tolera 10× sobre 1 min).
Ver [[dokploy-schedule-step-expression-no-catch-up-tras-caida]].
