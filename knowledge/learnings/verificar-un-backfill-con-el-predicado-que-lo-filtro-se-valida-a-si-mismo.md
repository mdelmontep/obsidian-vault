---
title: verificar un backfill con el mismo predicado que lo filtró se valida a sí mismo
date: 2026-08-06
source: claude-code-session facturaia
tags: [postgres, migraciones, verificacion, testing]
---

Variante del guard vacío, y más difícil de ver: el `DO $$` de la migración
comprueba «¿queda alguna fila mal?» usando **el mismo WHERE que acotó el INSERT**.
Cualquier fila que el predicado excluyera por estar mal formulado queda fuera de
las dos, y el guard canta verde.

Caso TuFacturaIA (mig 644): el backfill filtraba `pendiente_eur > tolerancia` y la
verificación preguntaba exactamente eso → «0 pendientes». Pero los ABONOS tienen
total negativo y la función les clampa el pendiente a 0, así que ni entraban en el
INSERT ni salían en el check. **Seguían cayendo 99 de las 108 negativas** y el guard
cantaba verde: 88 emitidas con total negativo (rectificativas importadas como
facturas), 7 abonos `cobrada` y 4 `vencida`. Cerrado en la mig 645, que pasa el
objetivo a `ABS(...)` para que el respaldo sea representable y hace el backfill.

- Lo destapó **volver a ejecutar la operación real** (correr el recompute y mirar el
  estado antes/después), no una consulta con el mismo predicado.
- Y el radio se mide sobre la población COMPLETA. La primera medición dio «7» por
  muestrear las 60 más recientes; el número real era 99. Muestrear al medir un
  radio es el mismo error que verificar con el predicado del filtro: te devuelve
  lo que ya creías.
- Regla: la verificación tiene que atacar el EFECTO observable (¿se mueve el dato?),
  con un criterio **independiente** del que seleccionó las filas.
- Corolario de signo: cualquier acotación con `> 0` / `> tolerancia` sobre importes
  es ciega a los documentos negativos (abonos, rectificativas, devoluciones).
  Comprobar el censo por `tipo_documento`, no solo el total.

Hermano de [[guard-de-migracion-que-recalcula-la-formula-no-verifica-nada]] ·
[[convertir-columna-en-derivada-exige-backfill-del-historico]]
