---
title: el aviso y el panel que lo resuelve tienen que medir la misma ventana
date: 2026-08-26
source: facturaia
tags: [correccion, guards, ux, sql]
---

Una superficie AVISA («tienes albaranes sin cruzar, ¿seguro que apruebas?») y
otra RESUELVE (el panel donde los cruzas). Si el aviso mira una ventana más
estrecha que el panel, la rendija es exactamente el conjunto de casos que nadie
ve y nadie cruza — ahí entraba el doble conteo de stock.

Dos formas de estrecharla sin notarlo: **la constante duplicada** (el panel
importaba `DIAS_VENTANA_DEFECTO`, el aviso llevaba su número a mano) y **el nulo
invisible** (`between desde/hasta` excluye `fecha IS NULL`, así que un documento
sin fecha queda fuera del aviso para siempre → `or(fecha.is.null, and(gte…,lte…))`).

Regla: quien avisa y quien remedia comparten el predicado, o el aviso no es red,
es colador. El test se muta estrechando la ventana: si no cae, no mide.
Ver [[un-canal-de-avisos-solo-se-verifica-mirando-el-canal]].
