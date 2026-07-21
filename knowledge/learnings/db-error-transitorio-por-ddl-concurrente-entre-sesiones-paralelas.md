---
title: db_error simultáneo en endpoints no relacionados puede ser ddl concurrente de otra sesión, no bug de código
date: 2026-07-21
source: claude-code-session
tags: [supabase, postgres, multi-sesion, debug]
---
Con varias sesiones Claude Code trabajando en paralelo sobre el MISMO Supabase, un `db_error` que aparece a la vez en dos endpoints sin relación (presupuestos + calendario de personal) no significa que ambos tengan un bug — puede ser una query cancelada por `statement timeout` mientras otra sesión aplicaba una migración de RLS/Realtime a las mismas tablas en ese instante (lock de DDL).

Diagnóstico: `mcp__supabase__get_logs(service:'postgres')` → busca `"canceling statement due to statement timeout"` cerca de la hora del reporte. Si aparece una sola vez y las queries del endpoint corren en milisegundos al reproducirlas a mano (`execute_sql` con `set local statement_timeout`), es transitorio — no cambies código a ciegas. Verifica con `git log origin/main` si hay migraciones DDL de otra sesión mergeadas justo en esa ventana horaria.

Caso real: TuFacturaIA, `db_error` en `/obras/presupuestos` y `/obras/personal` coincidiendo con mig 540/542/544 (RLS + Realtime) de otra sesión paralela.
