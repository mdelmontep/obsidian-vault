---
title: Cron detector de drift debe usar el MISMO rango que generó el snapshot
date: 2026-06-12
source: facturaia PR #214 — falsos "Declaración 130 desactualizada"
tags: [cron, snapshot, fiscal, supabase]
---

Un cron que detecta drift comparando "estado live vs snapshot persistido" debe
reconstruir el conjunto live con **exactamente la misma query/rango** que usó
quien escribió el snapshot. Si el productor es acumulado (modelo 130 = YTD,
1 ene → fin trimestre) y el detector usa solo el trimestre, todo lo anterior
aparece como "saliente" → falso positivo en cada run, amplificado si la notif
se reabre como no leída en cada upsert (`notify_upsert` borra `notification_reads`).

Regla: extraer el cálculo de rango a un helper compartido o espejarlo con
comentario cruzado + test de regresión (snapshot YTD → `sin_cambios`).

Caso: [[facturaia]] cron `fiscal-recalcular-borrador` vs `rangoYTD` de `calcular.ts`.
