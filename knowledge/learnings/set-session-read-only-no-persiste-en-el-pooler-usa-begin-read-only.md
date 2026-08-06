---
title: para leer prod sin poder escribir usa BEGIN READ ONLY, no SET SESSION ni options de conexión
date: 2026-08-06
source: claude-code-session
tags: [postgres, supabase, pooler, produccion, seguridad]
---
Consultando prod con `psql` por el pooler de Supabase (modo *transaction*), los
dos candados "obvios" NO funcionan y dan falsa seguridad:

- `?options=-c%20default_transaction_read_only%3Don` → el pooler lo ignora
  (`current_setting` devuelve `off`).
- `SET SESSION CHARACTERISTICS AS TRANSACTION READ ONLY;` → no persiste entre
  sentencias, porque cada una puede ir a otra conexión del pool.

Con ambos "activos" un `UPDATE` real pasó sin queja.

Lo que SÍ funciona, todo en la misma sentencia:
`psql -c "BEGIN READ ONLY; SELECT ...; COMMIT;"` → un `UPDATE` ahí dentro falla
con *cannot execute UPDATE in a read-only transaction*.

Y **verifica el candado antes de fiarte**, con una escritura real sobre tabla
permanente (`UPDATE t SET c = c WHERE false`). No sirve `CREATE TEMP TABLE`:
Postgres permite temporales dentro de transacciones read-only, así que esa
prueba pasa siempre y no discrimina.
