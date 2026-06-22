---
title: supabase-js devuelve PGRST205 (no 42P01) cuando la tabla no existe
date: 2026-06-22
source: claude-code-session
tags: [supabase, postgrest, errores]
---

Una feature que degrada con elegancia mientras su migración no está aplicada
(tabla ausente) debe detectar bien el error. Vía supabase-js (PostgREST) la tabla
inexistente NO da el `42P01` crudo de Postgres: da

> error.code === 'PGRST205'  ("Could not find the table '...' in the schema cache")

El `42P01` solo aparece por SQL directo (psql/db execute). Si el guard solo mira
`42P01`, el código rethrowea y la página crashea en vez de degradar.

Fix: en el guard mirar `code === 'PGRST205' || code === '42P01'` (+ nombre de
tabla). Lo cazó un smoke de datos read-only, no el typecheck/build.
