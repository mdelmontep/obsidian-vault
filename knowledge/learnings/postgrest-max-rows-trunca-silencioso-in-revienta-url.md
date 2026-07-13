---
title: postgrest trunca a 1000 filas en silencio y .in() grande revienta la url
date: 2026-07-03
source: claude-code-session
tags: [supabase, postgrest, paginacion, bugs-silenciosos]
---
Dos límites de PostgREST que fallan sin error visible en queries "sacar todo":
1. `db-max-rows` (Supabase hosted: 1000) corta el resultado SIN señal — un
   export/agregado sobre >1000 filas devuelve importes de menos y nadie se
   entera. Los embedded selects (`lineas:tabla(...)`) NO cuentan para el cap.
2. `.in(col, ids)` viaja en la URL del GET (~39 bytes/UUID): a partir de
   ~400-840 ids el edge corta la request → 500.
Patrón fix (FacturaIA `load-facturas-contables.ts` + `admin-connections.ts`):
chunkear ids a ≤150-500 por request y paginar con `.order(pk).range(from, to)`
en bucle hasta `page.length < PAGE_SIZE` (el order estable es obligatorio o
range salta/repite filas). Test: cliente fake que simula el cap de 1000.

Señal de diagnóstico: si pides `{ count: 'exact' }` el count SÍ es exacto (lo
calcula la BD), pero el importe (reduce en JS sobre filas truncadas) sale de
menos → count y cifra €/ quedan incoherentes entre sí; esa discrepancia delata
el truncado. Como las filas no van ordenadas, además el corte es no determinista.
