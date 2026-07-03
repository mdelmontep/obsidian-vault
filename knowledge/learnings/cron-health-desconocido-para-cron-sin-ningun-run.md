---
title: computeHealth trata un cron sin NINGÚN run histórico como 'desconocido', no 'rojo' — nunca alerta
date: 2026-07-03
source: claude-code-session
tags: [monitoring, crons, alerting, tufacturaia, dokploy]
---

`computeHealth(recentRuns, maxIntervalo)` devuelve `'desconocido'` si `recentRuns` está
vacío (`!latest → return 'desconocido'`). El collector de alertas (`cron_down`) solo
dispara si `health === 'rojo'` — así que un cron que **nunca ha corrido ni una vez**
(0 filas en `cron_runs`) NO genera alerta jamás, a diferencia de uno que corrió y luego
dejó de correr (eso sí cae en rojo por antigüedad del último run).

Caso real: `slack-dispatcher` llevaba desde su creación sin ningún schedule dado de alta
en Dokploy (`CRON_REGISTRY` del código es solo informativo, no garantiza que el schedule
real exista — ver [[dokploy-cron-pre-stage-disabled-si-endpoint-no-desplegado]]). 0 runs,
0 alertas, nadie lo detectó hasta una auditoría manual cron-por-cron comparando
`CRON_REGISTRY` contra `schedule.list` real de Dokploy.

Fix pendiente: tratar "0 runs desde que el cron existe en el registro con antigüedad >
max_intervalo" como rojo también, no solo "último run viejo". Mientras tanto: auditar
periódicamente `CRON_REGISTRY` vs `schedule.list` de Dokploy, no fiarse solo del panel
de alertas para detectar crons fantasma.

Relacionado: [[cron-health-flapea-con-run-en-vuelo-sobre-error]], [[alert-collector-cron-vs-live-dedup-gap]].
