---
title: filtro postgrest por una columna pierde filas si el criterio real es coalesce(a,b)
date: 2026-07-11
source: claude-code-session
tags: [supabase, postgrest, sql, coalesce]
---
Si el particionado real de una tabla es `COALESCE(fecha_operacion, fecha)` pero el filtro SQL usa solo `.gte('fecha',...).lte('fecha',...)` con re-filtro en memoria por el COALESCE, una fila con `fecha` fuera del rango pero `fecha_operacion` dentro NUNCA llega ni al SQL ni al filtro en memoria — desaparece de TODOS los periodos, no solo del actual.

**Fix real**: replicar el COALESCE exacto con `.or()` de dos ramas excluyentes:
`and(col_b.gte.X,col_b.lte.Y),and(col_b.is.null,col_a.gte.X,col_a.lte.Y)` — ya usado en el repo con `.or('created_at.lt.X,and(...))'`. Nunca "ampliar la ventana un día" como parche — no cubre el caso real (desfases de días/semanas).

Caso real: TuFacturaIA, `cargarFacturasPeriodo` — una factura con `fecha`/`fecha_operacion` en trimestres distintos quedaba fuera de todos los modelos fiscales sin ningún cuadre que avisara.
