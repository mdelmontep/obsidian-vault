---
title: comparar una fecha 'YYYY-MM-DD' contra un timestamptz ISO como strings falla
date: 2026-07-17
source: claude-code-session
tags: [postgres, js, fechas, gotcha]
---
Comparar lexicográficamente un día `'YYYY-MM-DD'` (10 chars) contra un valor que en realidad es
TIMESTAMPTZ / ISO completo (`'2026-07-17T20:02:45+00:00'`) da resultados MAL:
- `'2026-07-17' >= '2026-07-17T20:02…'` → FALSE (el prefijo de 10 chars es "menor" que el string
  con hora) → un rango [apertura, cierre] "pierde" justo el primer día.
- `fecha.split('-').reverse().join('/')` sobre un timestamp produce basura ("17T20:02.../…").
El origen del bug: se asume que la columna es DATE cuando es TIMESTAMPTZ (o la RPC/`select('*')`
la devuelve con hora). Fix: **normalizar con `.slice(0,10)` antes de comparar/formatear** (o
castear a `::date` en SQL). Caso real (obras): picó DOS veces en la misma sesión — `obraActivaEnDia`
(helpers del calendario) y `obra-row` (formato de fecha). Al tocar cualquier comparación/format de
fecha, verifica el TIPO real de la columna. Relacionado:
[[postgres-asumir-columna-existente-en-trigger-rewrite-verifica-information-schema]].
