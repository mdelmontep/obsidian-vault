---
title: un RETURNS TABLE no lleva tipos comprobados ni nulabilidad, y las dos cosas muerden después
date: 2026-08-14
source: claude-code-session
tags: [postgres, supabase, migrations, tipos]
---

Dos gotchas del mismo hueco: `returns table (...)` es una DECLARACIÓN, no un contrato verificado.

**1 · Los tipos se comparan al EJECUTAR, columna a columna.** Declarar `email text` sobre un
`select p.email` donde la columna es `citext`: `create function` la acepta **sin una palabra** —el
editor de SQL dice «Success»— y la primera llamada muere con `structure of query does not match
function result type … Returned type public.citext does not match expected type text in column 3`.
No lo ve ningún gate estático ni un test con dobles: sólo ejecutar la función contra un Postgres
real. Fix: cast explícito (`p.email::text`) y declarar el tipo que consume la aplicación.

**2 · No lleva nulabilidad, así que `supabase gen types` asume NO NULO todas las columnas.** Si la
tabla origen las tiene nulables, TypeScript te promete `string` donde llega `null`.

Corolario de método: una migración que no se ha EJECUTADO nunca no está verificada, por bien
razonada que esté. Levantar un Postgres desechable y llamar a la función es lo único que los caza.
Ver [[una-correccion-de-tipos-sobre-un-parser-que-recibe-unknown-es-inerte]].
