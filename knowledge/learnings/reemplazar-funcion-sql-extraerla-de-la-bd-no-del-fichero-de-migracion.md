---
title: para reescribir una función sql, extrae el cuerpo vivo con pg_get_functiondef
date: 2026-07-29
source: claude-code-session
tags: [postgres, migraciones, supabase]
---
Para cambiar una línea de una función que ya corre en producción, la tentación es
copiar el `CREATE OR REPLACE` del fichero de migración que la creó. Es un error:
migraciones posteriores le han cambiado `search_path`, grants o el cuerpo, así que
publicar esa copia **revierte en silencio** todo lo posterior.

Fuente de verdad = la base de datos:

```sql
select pg_get_functiondef(p.oid) from pg_proc p
  join pg_namespace n on n.oid = p.pronamespace
 where n.nspname='public' and p.proname='mi_funcion';
```

Volcarlo, parchear el trozo concreto con un script (no a mano), y meter el resultado
en la migración nueva. Añadir `pg_get_functiondef(...) LIKE '%<marca>%'` en el bloque
de verificación para que aborte si el parche no entró. `pg_get_functiondef` no termina
en `;` — hay que añadirlo. Caso real: TuFacturaIA migs 585 y 587 (`merge_cliente`,
`merge_proveedor`, `convertir_presupuesto_a_factura`, tocadas antes por las migs
252/320/336/576).

Reincidió el 30-ago (mig 772): el `;` que falta no lo ve ninguna revisión a ojo, lo ve
un Postgres. **Parsea la migración antes de mergear** contra el proyecto de staging,
`BEGIN` + `\i fichero` + `ROLLBACK`, y mira el `ec`.

Y ojo al usar `pg_get_functiondef` para verificar la AUSENCIA de algo (10-sep, mig 884):
devuelve también los **comentarios** del cuerpo, así que un `NOT LIKE '%<marca>%'` da falso
positivo por una línea `-- ... <marca> ...` que no ejecuta nada. La autoverificación tiene
que filtrar los comentarios antes de buscar; si no, o aborta una migración correcta, o te
hace investigar un fallo que no existe. Ya había mordido en las migs 744 y 827.
