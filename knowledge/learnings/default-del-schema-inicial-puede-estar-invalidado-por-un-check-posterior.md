---
title: copiar un default del schema inicial arrastra un valor que un check posterior invalidó
date: 2026-08-18
source: claude-code-session
tags: [supabase, migraciones, postgres, gotcha, facturaia]
---

Al escribir una migración que inserta en una tabla vieja, el `DEFAULT` que ves en su
`CREATE TABLE` original puede llevar meses inválido: una migración posterior añadió un
CHECK y actualizó el default VIVO sin tocar el fichero histórico, que sigue en el repo
diciendo lo de antes.

Caso (TuFacturaIA, mig 708): copió `{codigo}{anio}-{num:04d}` del `001_schema.sql:116`.
La mig 021 había introducido `is_valid_series_format`, que solo admite otro juego de
tokens → **23514 a mitad de `db push` contra producción**. El fichero de la 001 sigue
mintiendo hoy; el default real en prod ya era `{CODIGO}{AAAA}-{NNNN}`.

- La referencia es PROD, no el primer fichero: `information_schema.columns.column_default`,
  y si hay función de validación, llamarla (`select is_valid_series_format('…')`).
- Mejor aún: copiar de una **fila real** de la tabla. Las 7 series de esa org ya traían el
  formato bueno.
- Lo que salvó la situación: `BEGIN`/`COMMIT` **explícitos** en la migración → rollback
  total, cero estado a medias. Sin ellos, los 13 statements previos quedan aplicados y sin
  fila en `schema_migrations`, que es el peor sitio donde pararse.
- Corolario: cuando una migración larga falla, auditar contra el catálogo **todos** los
  statements siguientes antes de reintentar — no se han ejecutado nunca.

Ver [[suite-filtrada-por-carpetas-del-pr-no-ve-los-guards-de-arquitectura]] ·
[[el-hueco-libre-de-migraciones-puede-estar-ya-ocupado-en-produccion]]
