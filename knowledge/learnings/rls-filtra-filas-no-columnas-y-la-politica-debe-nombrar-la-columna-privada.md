---
title: rls filtra filas, no columnas, y la política debe nombrar la columna privada
date: 2026-07-28
source: claude-code-session
tags: [supabase, rls, postgres, seguridad]
---

Una tabla de mensajes con columna `internal boolean` y política "el dueño ve su
hilo" filtra por dueño, no por `internal`: el cliente lee por PostgREST con su
propio JWT los mensajes internos de SU ticket. Confirmado en prod (FacturaIA:
las instrucciones que le pasábamos a Claude eran legibles por el cliente).

Y RLS **no oculta columnas**. Aunque la política acierte, `select *` sobre la
tabla padre devuelve `notas_internas`, `admin_visto_at`, etc. Eso solo se corta
con grants por columna:

```sql
revoke select on t from anon, authenticated;
grant select (col_publica_1, col_publica_2, ...) on t to authenticated;
```

Regla: columna privada en tabla que el usuario puede leer → (a) nómbrala en el
`using` si decide visibilidad de fila, y (b) fuera de la lista del `grant`.
Al aplicar el grant por columnas, grep de los consumidores con sesión de
usuario: un `select *` con el cliente del navegador pasa a 42501.
Ver [[verificar-grants-por-columna-con-pg-attribute-attacl-no-con-information-schema]].
