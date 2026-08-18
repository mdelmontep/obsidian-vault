---
title: un \i de migración dentro de tu BEGIN ejecuta su COMMIT y te confirma el DDL
date: 2026-08-18
source: claude-code-session
tags: [postgres, psql, supabase, migraciones, produccion, gotcha]
---
Ejercitar SQL contra producción dentro de `BEGIN … ROLLBACK` es la técnica correcta, pero
**no vale cargar el fichero de migración con `\i`**: si la migración abre su propio
`BEGIN; … COMMIT;` (lo correcto en este repo), su `COMMIT` **cierra tu transacción de
prueba** y confirma el DDL. El `ROLLBACK` final ya no tiene nada que deshacer.

Medido (TuFacturaIA, mig 710): psql avisa con un `WARNING: there is already a transaction
in progress`, que se lee como inocuo, y la función quedó **creada en producción** antes de
tiempo. Lo destapó comprobar el residuo al salir, no el `ec=0` del script.

- Copia el CUERPO del objeto dentro de tu transacción, sin el `\i`.
- Mide el residuo SIEMPRE al terminar (`to_regclass`, `pg_proc`, contar filas): un
  `ROLLBACK` que aparenta éxito no prueba que no quedara nada.
- Si ya se aplicó y el fichero es idempotente de arriba abajo, se cierra aplicándolo por
  `db push`, que lo reaplica y **lo registra**. Dejarlo sin registrar es la deriva que hace
  que `db push` se salte la migración sin error más adelante.

Ver [[smoke-trigger-sql-tx-rollback-contra-prod]] ·
[[schema-migrations-no-es-source-of-truth-si-aplicas-manual]]
