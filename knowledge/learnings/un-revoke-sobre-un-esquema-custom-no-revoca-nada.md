---
title: un revoke sobre un esquema custom no revoca nada, y el test pasa igual
date: 2026-09-05
source: mandadm
tags: [postgres, supabase, seguridad, tests]
---

`create schema ops; revoke all on schema ops from anon, authenticated;` **no hace nada**: Postgres no
concede `USAGE` a `PUBLIC` sobre un esquema creado a mano (a diferencia de `public`, que sí lo trae
del bootstrap). Lo mismo con los `alter default privileges ... revoke all` que se ponen «por si acaso».

Peligro real: el test que «demuestra» el candado —`select` como `anon` sobre una tabla de `ops`, que
falla— pasa **por el comportamiento por defecto**, no por tus líneas. Medido con mutación contra
Postgres 17: quitando las cuatro líneas de la migración, la suite sigue verde. Un candado con cero
efecto observable y un test que no distingue.

Fix: el test no pregunta «¿falla el select?», pregunta por el privilegio.
`has_schema_privilege('anon','ops','usage')` debe ser false, y `pg_default_acl` no debe tener entrada
para el esquema. Esas dos sí tienen víctima: inyecta `grant usage on schema ops to anon` y se ponen
rojas. Y deja escrito en la migración que el `revoke` es seguro contra un `grant` futuro, no la
puerta cerrada — o el siguiente lector cree que protege.

Inverso de [[postgres-revoke-public-no-elimina-grants-individuales]] (allí el grant sobra; aquí el
revoke no existía). Ver [[una-pieza-con-su-suite-en-verde-que-el-sistema-no-llama]].
