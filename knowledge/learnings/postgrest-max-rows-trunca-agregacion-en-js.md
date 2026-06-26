---
title: postgrest trunca agregaciones hechas en js por el cap max-rows (default 1000)
date: 2026-06-26
source: claude-code-session
tags: [supabase, postgrest, performance, bug]
---

Agregar (sumar/contar importes) trayendo las filas y haciendo `reduce` en JS sobre
una tabla grande es un bug silencioso: PostgREST corta la respuesta en `max-rows`
(default **1000**), así que la suma sale **infravalorada** sin error. Peor: si pides
`{ count: 'exact' }`, el `count` SÍ es exacto (lo calcula la BD) → la cifra €/ y el
count quedan **incoherentes** entre sí. Y como las filas no van ordenadas, el truncado
es no determinista.

Fix: agregar en BD, no en JS.
- RPC `SECURITY DEFINER` que devuelva `SUM()/COUNT()` en una pasada (lo más limpio), o
- `.order(col).limit(N+1)` + flag `truncated` que el consumidor verbalice/avise.

Síntoma típico: "el total que me dice el copiloto/informe es menor que el real solo en
orgs grandes". Caso: KPIs del copiloto FacturaIA (`getKPIs.ts`, `compararEmpresas.ts`;
la deuda sin filtro de fecha es el peor caso). El hermano `getDeudaPorCliente.ts` ya lo
hacía bien (limit+truncated) → replicar ese patrón.
