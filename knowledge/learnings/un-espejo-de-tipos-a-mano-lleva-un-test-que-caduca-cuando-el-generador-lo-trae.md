---
title: un espejo de tipos escrito a mano lleva un test que caduca cuando el generador lo trae
date: 2026-08-31
source: tucrmia
tags: [typescript, migraciones, supabase, deuda]
---
Con migraciones escritas y sin aplicar, los tipos generados (`gen:types`) no traen todavía sus
funciones, así que hay que escribir el espejo a mano. Ese espejo es deuda que nadie recuerda: sigue
ahí meses después, tapando la firma real y divergiendo de ella sin avisar.

El candado: junto al espejo, un test que AFIRMA que los tipos generados **no** traen aún esa
función. El día que la migración entra, el test se pone rojo y su mensaje dice qué borrar.

Se pagó solo: al aplicar 29 migraciones pendientes, tres candados se pusieron rojos a la vez y cada
uno nombró su espejo. Sin ellos, tres copias a mano habrían sobrevivido a la verdad que duplicaban.
Regla general: **toda copia a mano de algo generado lleva su propia caducidad ejecutable**, no un
`// TODO: borrar cuando`. Ver [[un-catalogo-de-capacidad-de-un-tercero-escrito-a-mano-miente-en-silencio]].
