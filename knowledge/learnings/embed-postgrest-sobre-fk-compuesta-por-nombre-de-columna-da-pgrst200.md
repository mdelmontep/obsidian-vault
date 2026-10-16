---
title: embed de postgrest sobre fk compuesta nombrado por columna da pgrst200
date: 2026-10-17
source: agency-portal (incidente 5→16-oct, panel de tareas vacío)
tags: [supabase, postgrest, fk]
---
- `select('*, x:otra_tabla!<columna>(...)')` desambigua por COLUMNA. Si la FK es compuesta (p. ej. `(agency_id, <columna>)`), PostgREST no la encuentra con una sola columna y responde `PGRST200` («Could not find a relationship…»).
- supabase-js no lanza: devuelve `{ data: null, error }`. Con `if (error) return []` delante, la pantalla sale vacía y nadie se entera. En agency-portal fueron 11 días.
- Fix: desambiguar por NOMBRE DE CONSTRAINT (`otra_tabla!<nombre_de_la_fk>(...)`, sacado de `pg_constraint`), que vale tanto para una FK simple como para una compuesta.
- Antes de desplegar, comprobar el select contra el PostgREST real (`limit=0`). El `typecheck` no lo caza, porque el string del select no se valida contra el esquema compuesto.
- En agency-portal ya hay red de seguridad: `readFailed()` + guard AST + `/api/internal/health-schema` barrido por `ops/portal-db-probe`. Ver [[filtro-texto-libre-a-columna-tipada-error-tragado-parece-vacio-real]].
