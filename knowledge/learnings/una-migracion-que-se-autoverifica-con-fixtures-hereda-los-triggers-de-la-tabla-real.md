---
title: una migración que se autoverifica con fixtures hereda los triggers de la tabla real
date: 2026-08-17
source: claude-code-session facturaia
tags: [postgres, supabase, migraciones, triggers, testing]
---

Meter un caso construido dentro de la propia migración (INSERT de fixtures + assert +
`ROLLBACK TO SAVEPOINT`) parece gratis: nada se commitea. El riesgo no es que ensucie, es
que **falle**. Esos INSERT disparan todos los triggers de la tabla real, y si alguno no
tolera una fila sintética de cuatro columnas, aborta la migración entera por algo que no
tiene nada que ver con lo que venía a hacer.

Caso TuFacturaIA (#1703, mig 702): el fixture insertaba en `organizations`, que tiene
**seis triggers** en producción, dos de ellos `AFTER INSERT` que siembran filas en otras
tablas (`trigger_org_series_abono_proforma` mig 211, `trg_obras_seed_tipos_unidad` mig 476).
Se había verificado contra un esquema mínimo hecho a mano, que no tenía ninguno: las dos
pasadas en verde no ejercitaban ese camino.

- Dentro de una migración, los asserts van **de solo lectura**: `count(*)`, `information_schema`,
  `PERFORM <fn>()`. Eso sí cabe y es determinista.
- Un caso construido con datos es un **test**, y vive en el arnés de tests. Si el repo no
  tiene arnés SQL, la salida honesta es escribir en el comentario que no hay gate automático
  y con qué números se comprobó a mano — no fabricar infraestructura nueva para una tarea puntual.
- Antes de insertar en una tabla para probar algo, `grep -i "trigger.*on <tabla>"` sobre las
  migraciones. Lo que sabe la tabla real nunca lo sabe el esquema de juguete.

Pariente de [[supabase-errores-que-solo-afloran-contra-schema-real]]
