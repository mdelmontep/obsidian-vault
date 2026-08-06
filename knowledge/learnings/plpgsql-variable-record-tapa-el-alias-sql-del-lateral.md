---
title: una variable RECORD de plpgsql tapa el alias SQL con el mismo nombre
date: 2026-08-06
source: claude-code-session facturaia
tags: [postgres, plpgsql, migraciones, debug]
---

Dentro de un `DO $$`/función plpgsql, si declaras `r RECORD` y una consulta del
cuerpo usa `r` como alias (típico: `CROSS JOIN LATERAL mi_funcion(x) r`), plpgsql
resuelve `r.campo` contra **su variable**, no contra el alias. Error:

```
ERROR: record "r" is not assigned yet
```

Que no dice nada del alias y manda a buscar el bug donde no está.

Caso TuFacturaIA (mig 644): el bloque de verificación declaraba `r RECORD` para un
`FOR r IN …` y más arriba tenía
`CROSS JOIN LATERAL public.factura_cobros_resumen(f.id) r WHERE r.pendiente_eur > …`.
Reventó tras insertar 1.312 filas (el ensayo con ROLLBACK lo cazó antes de aplicar).

- Fix: nombrar las variables plpgsql con prefijo (`v_row`) y los alias SQL con algo
  distinto (`res`). Convención que además hace el cuerpo legible.
- Aplica a cualquier nombre, no solo `r`: si el alias coincide con una variable
  declarada, gana la variable.

Relacionado: [[plpgsql-array-mas-literal-sin-cast-se-resuelve-como-array]]
