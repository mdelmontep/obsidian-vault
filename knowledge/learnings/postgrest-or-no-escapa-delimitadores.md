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
Ver [[agrupacion-por-campo-texto-libre-exige-normalizacion-en-write-path]].
