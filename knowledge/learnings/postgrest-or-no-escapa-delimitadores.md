---
title: postgrest .or() no escapa sus delimitadores — comas/paréntesis en el valor rompen el filtro
date: 2026-07-13
source: claude-code-session
tags: [supabase, postgrest, bug]
---
`escapeIlike` (escapar `%`/`_`/`\`) NO basta si el valor va dentro de un
`.or('nombre.ilike.%X%,nif.ilike.%X%')`: PostgREST parsea la lista de `.or()` por
comas/puntos/paréntesis, así que un valor con coma ("García, S.L.") **parte la lista
de condiciones** → error PostgREST, cero match. Se manifestó como `listarClientes`
56% OK, con la causa enmascarada por un `throw` genérico que descartaba el error real.

Fix: entrecomillar el valor para PostgREST — `nombre.ilike."%valor%"` — escapando `\`
y `"` dentro de las comillas; `%`/`_` siguen siendo wildcards. Dos capas de escape:
escapeIlike (capa SQL) + comillas (capa transporte). Y no enmascarar el error: loguea
`error.message` antes del throw. Aplica a cualquier `.or()` con texto de usuario en supabase-js.
Usa el helper `orIlikePattern` (entrecomilla) en vez de `escapeIlike` dentro de un `.or()`.

REGRESIÓN 2026-07-18 (Obras F3): el bug volvió en 2 tools de copiloto nuevas. El test las daba
VERDES porque **mockea `.or()` como no-op** → nunca ejercita la construcción de la query, solo el
happy path. El gate por-issue no lo vio; lo cazó el gate de cierro cross-issue LEYENDO el código.
Moraleja: un mock del query-builder no valida el string que se le pasa — grep de `escapeIlike`
dentro de `.or(` como chequeo barato, y no fíes la cobertura de un `.or()` a un test con mock no-op.
Ver [[agrupacion-por-campo-texto-libre-exige-normalizacion-en-write-path]].
