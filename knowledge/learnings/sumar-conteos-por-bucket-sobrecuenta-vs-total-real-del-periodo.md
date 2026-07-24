---
title: sumar conteos por bucket sobre-cuenta frente al total real del periodo
date: 2026-07-25
source: claude-code-session
tags: [time-tracking, agregacion, metricas]
---

Un gráfico bucketizado (por hora/día) que cuenta "¿hubo actividad de X en ESTE bucket?"
da 1 por cada bucket que una sesión/entidad cruza. Sumar esos conteos a lo largo de
todas las filas para obtener un "total del periodo" SOBRE-CUENTA: una sesión de 3h
que cruza 3 buckets de 1h cuenta como 3, no como 1.

**Horas SÍ es seguro sumar** — la duración se reparte sin solape entre buckets
(overlap partition), la suma de los trozos da el total exacto. **Conteos discretos
(nº de sesiones, nº de entidades distintas) NO** — hay que recalcular el total sobre
los datos crudos filtrados por rango (contar IDs/valores distintos), nunca sumando
el conteo-por-bucket.

Caso real: panel "Total del periodo" mostrando "18 técnicos" con solo 3 en el
equipo, al sumar el conteo-por-bucket de una métrica de distintos en vez de contar
distintos reales en `[since, until]`.

Ver `periodTotalsByKey` en `agency-portal/src/lib/time-tracking/aggregate.ts`.
