---
title: reintentar la suite que muere tapa un dato aleatorio que viola un constraint
date: 2026-09-29
source: facturaia
tags: [tests, flaky, reintento, postgres, gates]
---

Un gate que reintenta las suites de integración «sin síntoma de código» dio verde a la segunda sobre un
test roto: generaba un año aleatorio entre 2190 y 2219 contra un CHECK que topa en 2200. El reintento
sacó otro número válido y el defecto pasó por flake.

Patrón: el reintento solo es honesto para fallos que el dato NO decide. Una violación de constraint
(clase 23 de Postgres: `23514/23505/23503/23502`, «violates … constraint») es del código o del test,
así que no se reintenta y bloquea. Excepción por NOMBRE, no por clase: los CHECK que comparan una marca de
tiempo con `created_at` sí los viola un reloj desfasado de la VM sin defecto ninguno.

Orden de la clasificación: síntoma de código clásico > CHECK de reloj por nombre > clase 23 > reloj
genérico > desconocido. Lo desconocido se sigue reintentando mientras no haya datos para cambiarlo.
Caso: facturaia #3096, `scripts/lib/integracion-medida.mjs`.
Ver [[la-suite-completa-bajo-paralelismo-no-distingue-regresion-de-saturacion]]
