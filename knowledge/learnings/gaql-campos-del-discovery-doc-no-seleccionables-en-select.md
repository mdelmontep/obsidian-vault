---
title: gaql — la seleccionabilidad es por mensaje, no por hoja (y el discovery doc no la promete)
date: 2026-08-21
source: facturaia
tags: [google-ads, gaql, api, gotcha]
---
En Google Ads v25 la seleccionabilidad GAQL es a nivel de MENSAJE: `SELECT
recommendation.impact` o `recommendation.campaign_budget_recommendation` (los padres)
→ 200 con el mensaje entero y sus subcampos; sus hojas
(`...recommended_budget_amount_micros`, `impact.base_metrics.clicks`) NI EXISTEN como
campos y responden `400 Unrecognized fields`, aunque el discovery doc las liste en el
shape (shape ≠ selectability). Medido en vivo el 21-ago-2026.

Fuente autoritativa: `GoogleAdsFieldService` (`googleAdsFields:search`, `SELECT name,
selectable, filterable WHERE name LIKE 'recommendation%'`) — consultarla ANTES de
construir sobre el discovery doc. Y ojo al `WHERE resource_name`: con un id malformado
(no numérico) da 500 INTERNAL, no 400 — no confundirlo con un campo no filtrable.

Caso real: card de FB-08 en 400 desde su merge (#2031, fix #2041: seleccionar los 2
padres; el parse ya esperaba ese shape). El analista FB-09 usa la query ligera de conteo.
