---
title: gaql — campos que el discovery doc lista pueden ser no seleccionables en SELECT
date: 2026-08-21
source: facturaia
tags: [google-ads, gaql, api, gotcha]
---
La forma del mensaje en el discovery doc de Google Ads NO implica seleccionabilidad GAQL:
v25 rechaza con `400 Unrecognized fields` un SELECT de `recommendation.impact.*` y
`recommendation.campaign_budget_recommendation.*` aunque ambos existen en el recurso
`recommendation` (medido en vivo contra la cuenta real el 21-ago-2026). Los campos base
(`resource_name`, `type`, `dismissed`, `campaign`) y `customer.optimization_score` sí pasan.

Fix/patrón: antes de fiarse del doc, sondear con `searchStream` variantes de la query real
(script tipo `probe-gaql.mjs`: base / impact / budget / score por separado) y construir la
feature sobre lo que la API acepta, no sobre lo que el doc enumera. Si solo hace falta el
conteo, query ligera de campos base con LIMIT y `tope_alcanzado`.

Caso real: la card de recomendaciones de FB-08 daba 400 en prod (issue #2031); el analista
FB-09 lo esquivó con `conteoRecomendacionesActivas` (PRs #2032/#2034).
