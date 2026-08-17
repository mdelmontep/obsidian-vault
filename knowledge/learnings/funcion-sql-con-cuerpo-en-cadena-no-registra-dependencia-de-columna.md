---
title: una función sql con el cuerpo en cadena no registra dependencia de columna, así que el drop la rompe en silencio
date: 2026-08-17
source: claude-code-session facturaia
tags: [postgres, supabase, migraciones, drop-column, 42703]
---

`CREATE FUNCTION … LANGUAGE sql AS $function$ … $function$` guarda el cuerpo como
**texto**: Postgres no anota nada en `pg_depend` sobre las columnas que usa. Un
`DROP COLUMN` de una columna que la función lee **no falla** — se aplica limpio y la
función queda apuntando a algo que ya no existe, reventando con `42703` en su primera
ejecución. Una vista sí bloquearía el DROP; una función así, no.

Caso TuFacturaIA (#1703, mig 702): `admin_dashboard_stats()` valoraba el tramo de add-ons
del MRR con `plan_features.addon_price_eur`. El DROP de esa columna habría tumbado
`/admin` entero en la primera carga. No lo vieron ni `tsc`, ni el lint, ni 12.739 tests:
nada typechequea el interior de un cuerpo `plpgsql`/`sql`.

- Antes de un `DROP COLUMN`, **grep de la columna en `supabase/migrations/*.sql`**, no solo
  en el código de aplicación, y mira si algún hit está dentro de un `CREATE OR REPLACE
  FUNCTION`. Los seeds y el DML son ruido; las funciones son el riesgo.
- El arreglo es `CREATE OR REPLACE` de la función **en la misma migración y antes del DROP**.
- Y deja un `PERFORM <fn>()` en un `DO $$` dentro de la transacción: convierte «creo que no
  revienta» en «aborta la migración si revienta».
- El `BEGIN ATOMIC` de PG14+ sí registra dependencias, pero el estilo del repo es cadena.

Pariente de [[supabase-select-columna-inexistente-falla-query-entera-42703]] ·
[[column-list-drift-clientes-proveedores-select-inexistente-42703]]
