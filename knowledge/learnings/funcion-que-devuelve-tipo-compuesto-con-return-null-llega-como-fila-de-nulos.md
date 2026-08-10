---
title: una función que devuelve un tipo compuesto y hace `return null` llega como fila de nulos
date: 2026-08-11
source: claude-code-session
tags: [postgres, postgrest, supabase]
---
`create function reclamar() returns jobs` con `return null` dentro **no** llega al cliente como
`null`. Postgres materializa el NULL de un tipo compuesto como una fila con todas las columnas
nulas, y PostgREST la serializa tal cual: `{ id: null, peticion: null, … }`.

Un objeto así pasa cualquier `if (!x)`, así que el patrón habitual `return data ?? null` no lo
detecta y el consumidor revienta al leer el primer campo:
`TypeError: Cannot read properties of null (reading 'slice')`.

Fix: comprobar una columna que no pueda ser nula en una fila real — `data?.id ? data : null` — en
vez de comprobar el objeto.

Y probarlo con la cola **vacía**: el fallo solo aparece al agotar los trabajos, que es justo lo que
hace un worker en modo vigilancia cada pocos segundos, y no aparece nunca procesando de uno en uno.
