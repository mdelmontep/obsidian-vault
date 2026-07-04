---
title: cron de mantenimiento auto-sanable no debe paginar por email — severidad por criticidad, no solo umbral
date: 2026-07-04
source: claude-code-session
tags: [monitoring, cron, alerting, facturaia]
---
Afinar el umbral de cada cron uno a uno (2×intervalo, ver
[[watchdog-umbral-debe-tolerar-un-tick-perdido]]) es frágil: basta con que
UNO se quede corto para que un salto transitorio del scheduler dispare un
email ALTA por un no-evento. Recurrencia real: tras el fix #393 (2026-06-19),
`mcp-dcr-cleanup` seguía a 36h (<2×24h) → 2026-07-04 se saltó un disparo y
paginó igual, siendo una purga que borra 0 filas y se recupera sola.
Patrón durable: clasificar el cron por CRITICIDAD, no solo tunear tiempos.
Mantenimiento auto-sanable (purgas, limpiezas cuya "consecuencia si falla" es
"sin pérdida de datos, el siguiente run barre la cola") → severidad que NO
paginue: visible en panel, SIN email. Solo paginan (ALTA+email) los crons cuyo
fallo bloquea negocio/dinero/legal. Así la clase entera es segura por diseño,
no depende de acertar el umbral de cada uno.
Fix TuFacturaIA PR #703: campo `CronMeta.criticidad:'housekeeping'` → el
`cronsCollector` emite 'media' (el health-sweep solo emailea 'alta').
