---
title: un guard sobre SQL/PostgREST tiene que conocer el embed y el alias, o mira una sola forma
date: 2026-08-15
source: claude-code-session
tags: [gates, postgrest, supabase, sql, tucrmia]
---
Un guard que decide «¿esta consulta toca la tabla X?» buscando `'X'` entrecomillado entero reconoce
**una sola** de las formas de nombrarla. Las otras tres son sintaxis corriente, no rodeos exóticos:

- **Embed**: `.select('id, X(col)')` — el nombre viaja DENTRO de una cadena más larga, sin comilla
  pegada a la derecha. Trae las filas de la hija en la misma petición.
- **Variantes del embed**: `X!inner(...)`, `X!fk(...)`, y el alias `y:X(...)`. Todas acaban igual: el
  nombre seguido de `!` o de `(`.
- **Alias del `update`**: `update public.X o set …` — si la expresión exige `set` pegado al nombre, la
  sentencia entera es invisible.

Medido en TuCRMIA: tres guards distintos (`s5`, `trash`, la frontera del censo) tenían el mismo hueco, y
uno más lo tenía en el `update`. En cada caso el gate salía **verde** sobre el fichero real con la línea
prohibida escrita — o sea la respuesta que da cuando no ha mirado.

Regla: una sola definición de «así se nombra una tabla en PostgREST», compartida por todos los guards.
Tres copias son tres dueños del mismo hecho y la cuarta variante sólo la aprenden dos.

Misma familia que [[un-import-con-alias-apaga-un-gate-que-busca-texto]] y
[[gate-que-valida-por-patron-textual-rechaza-el-equivalente-mas-amplio]], en el otro lenguaje.
