---
title: un job con filtro de ámbito devuelve ok habiendo cubierto solo parte del lote
date: 2026-08-26
source: agency-portal
tags: [backfill, crons, falsos-verdes, runbooks]
---
Un endpoint de backfill con filtro por cliente (`?only=<client_id>`) responde
`{"ok":true}` describiendo lo que hizo **dentro del filtro**, no lo que faltaba
fuera. Escribí un paso de runbook para recuperar 3 interacciones perdidas con
`only=` en singular; las 3 estaban repartidas entre DOS clientes, así que
ejecutarlo tal cual habría recuperado 2, devuelto `ok` y dejado la tercera
huérfana con apariencia de tarea cerrada.
Patrón: en todo procedimiento con filtro de ámbito, el runbook lleva (a) la
lista COMPLETA de ids objetivo y de qué cliente es cada uno, (b) el valor del
filtro construido a partir de esa lista (`only=a,b`), y (c) una consulta de
cierre que cuente lo que sigue pendiente. La condición de éxito es el conteo a
cero, nunca el `ok` de la respuesta. Hermano de
[[un-flag-de-dry-run-que-el-reenviador-ignora-convierte-el-smoke-en-produccion]].
