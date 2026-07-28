---
title: verificar grants por columna con pg_attribute.attacl, no con information_schema
date: 2026-07-28
source: claude-code-session
tags: [postgres, supabase, seguridad, verificacion]
---

`information_schema.column_privileges` solo lista los grants en los que el rol
que consulta es grantor, grantee o miembro. Con un rol de solo lectura ajeno
(`claude_runner_ro`) devuelve **0 filas** aunque los grants existan: parece que
nadie tiene acceso, y da un "verificado" falso en las dos direcciones.

El catálogo sí es visible para cualquiera:

```sql
-- por columna
select attname, array_to_string(attacl, ', ')
from pg_attribute
where attrelid = 'public.t'::regclass and attnum > 0 and not attisdropped;
-- de la tabla (si aquí no aparece 'authenticated=...r', no hay SELECT de tabla)
select array_to_string(relacl, ', ') from pg_class where oid='public.t'::regclass;
```

`(sin acl propia)` en una columna = hereda el grant de tabla; si el de tabla ya
no tiene `r`, esa columna es ilegible. Ver
[[rls-filtra-filas-no-columnas-y-la-politica-debe-nombrar-la-columna-privada]].
