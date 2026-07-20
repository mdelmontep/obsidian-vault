---
title: el coalesce del total no cubre el desglose por grupo; un parse estricto lo zerifica todo
date: 2026-07-20
source: claude-code-session
tags: [sql, postgres, zod, pricing]
---
Al exponer el desglose por-línea de un agregado (CTE recursiva → `SUM` con `GROUP BY`),
el `COALESCE` del TOTAL no protege las entradas del array: un grupo cuyas filas no
casan el `CASE` (p. ej. una sub-unidad sin materiales) da `SUM = NULL` en ese grupo,
y `jsonb_build_object` sin `COALESCE` emite `{importe: null}`. El `SUM` del total sí
ignora ese NULL, así que el total sale bien y el bug pasa desapercibido.

Aguas abajo, un `z.number()` (no nullable) en el schema del elemento hace que
`safeParse` rechace TODO el objeto → el fallback zerifica el cálculo entero (precio 0
falso) aunque el total venía correcto.

Fix de doble capa: `COALESCE(...,0)` por línea en el SQL (origen) + campo `nullable→0`
en el parse, y que el parse conserve el total aunque el array falle.

Caso real FacturaIA: `obras_uo_calcular`, UO con sub-UO vacía mostraba 0 € (mig 532).
Lo cazó `/fia-cierre` (correctness), no el QA en vivo (que solo probó líneas con material).
