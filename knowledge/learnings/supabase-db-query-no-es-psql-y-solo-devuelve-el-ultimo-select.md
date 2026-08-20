---
title: supabase db query no es psql y solo devuelve el último select
date: 2026-08-20
source: facturaia
tags: [supabase, cli, sql]
---

`supabase db query --file x.sql --linked` manda el fichero a una API, no lo pasa por psql.
Dos consecuencias que cuestan una vuelta cada una:

- **Los metacomandos de psql no existen.** Un `\set org '...'` da `syntax error at or near "\"`.
  Los literales van inline (o se genera el SQL con sed).
- **Solo vuelve el resultado del ÚLTIMO statement.** Un script con seis `select` de
  comprobación devuelve el sexto y los otros cinco se pierden en silencio, que es peor que
  un error: parece que los pasos no dieron nada.

Para una comprobación de varios pasos: `create temp table`, un bloque `do $$ ... $$` que
inserte una fila por paso, y un `select` final. Eso sí devuelve la traza entera.

Y no confundirlo con `db execute`: **no existe**. Ver [[checklist-web-stack]].
