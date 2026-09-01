---
title: una función que devuelve un tipo compuesto y hace `return null` llega como fila de nulos
date: 2026-08-11
source: aula · agency-portal
tags: [postgres, postgrest, supabase, multi-tenant]
---
`create function reclamar() returns jobs` con `return null` dentro **no** llega al cliente como
`null`. Postgres materializa el NULL de un tipo compuesto como una fila con todas las columnas
nulas, y PostgREST la serializa tal cual: `{ id: null, peticion: null, … }`.

Un objeto así pasa cualquier `if (!x)`, así que el patrón habitual `return data ?? null` no lo
detecta. Fix: comprobar una columna que no pueda ser nula en una fila real — `data?.id ? data : null`.

**Reventar es el caso BUENO** (1-sep, agency-portal). Si el consumidor lee el primer campo, salta un
`TypeError` y te enteras. Si en cambio pasa ese `null` a un filtro opcional —`if (opts.agencyId)
q.eq(…)`— el filtro **se salta** y la consulta corre SIN acotar por tenant: sin excepción, sin
traza, 9-10 veces por tick. Un filtro opcional convierte «no hay fila» en «todas las filas».

Y probarlo con la cola **vacía**, que es lo que hace un worker en vigilancia. Ojo al stub del test:
el nuestro devolvía un `null` limpio que producción no manda nunca, así que 19 de 36 tests estaban
verdes sobre el guard roto. Ver [[un-stub-que-no-aplica-el-filtro-de-la-consulta-real-prueba-la-coincidencia]].
