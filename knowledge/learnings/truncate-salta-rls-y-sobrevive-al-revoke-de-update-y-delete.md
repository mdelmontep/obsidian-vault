---
title: truncate salta RLS y sobrevive a un revoke de update y delete
date: 2026-08-03
source: claude-code-session
tags: [postgres, supabase, rls, multi-tenant, seguridad, append-only]
---
`TRUNCATE` **no pasa por RLS**: ninguna política lo filtra. Vacía la tabla de todas las organizaciones
de un golpe, y un `revoke update, delete` —lo que sostiene un append-only— no lo impide.

Cómo aparece sin que nadie lo escriba: las migraciones revocan `select, insert, update, delete`
—los cuatro DML **enumerados**— sobre el `grant all` que Supabase concede por defecto. Los otros
cuatro siguen vivos: `TRUNCATE`, `REFERENCES`, `TRIGGER` y `MAINTAIN` (PG17, permite `reindex`).
En `tucrmia-prod`: `anon` y `authenticated` los tenían en las **doce** tablas, y `service_role`
sobre las dos append-only. Con el replay en verde y su rojo demostrado.

**Los privilegios se conceden por enumeración; NO se quitan por enumeración.** `revoke all` y
conceder lo justo. Y comprobar el **ACL efectivo** (`relacl`, `has_table_privilege`), nunca el texto
de la migración: el texto era correcto — lo que estaba mal era la resta con lo ya concedido.

Cerrar también los `alter default privileges`, o el arreglo dura hasta la siguiente tabla.
Ver [[el-replay-que-arranca-mas-limpio-que-produccion-es-ciego]] · [[rls-multi-org-active-vs-membership]]
