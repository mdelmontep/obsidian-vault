---
title: un genérico sobre el argumento de select() de supabase-js deja a tsc sin memoria
date: 2026-09-03
source: tucrmia
tags: [supabase, typescript, tsc, tipos]
---
Helper que recibe las columnas como parámetro y las pasa a `.select(columnas)`:
`function f<Columnas extends string>(db, columnas: Columnas) { return db.from('t').select(columnas) }`.
Con los tipos generados de la base, `tsc --noEmit` **muere por heap** (`ec 134`, sin error de
tipos): el parser de tipos de PostgREST intenta resolver la cadena genérica contra todas las
columnas de la tabla y explota combinatoriamente. No es la carga de la máquina: reproducible
en frío.

**Fix**: el parámetro de columnas va como `string` plano y el resultado se devuelve como
`readonly Record<string, unknown>[]` (doble cast, con el comentario del porqué al lado); el
llamante estrecha con `String(fila.x)`. Se pierde el tipado fino de esa lectura, y se gana
que el gate termine. Alternativa cuando las columnas son fijas: literal directo en `.select()`.

Ver [[castear-data-de-una-query-supabase-oculta-el-42703-que-el-tipo-ya-detecta]] · [[tsc-de-un-repo-grande-desborda-el-heap-por-defecto-de-node-aunque-corra-solo]].
