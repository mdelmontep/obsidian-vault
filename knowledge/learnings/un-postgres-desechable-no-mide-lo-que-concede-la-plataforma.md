---
title: un postgres desechable no mide lo que la plataforma concede por defecto
date: 2026-09-10
source: mandadm
tags: [supabase, postgres, permisos, testing, gate, seguridad]
---
Supabase deja puestos unos `alter default privileges` que conceden **ALL** sobre toda tabla nueva de
`public` a `anon`, `authenticated` y `service_role`. Eso **desactiva** cualquier diseño de permisos
por columna: `0001_init.sql` de mandadm concedía el UPDATE columna a columna para dejar fuera
`ig_user_id`; medido recién desplegado, `accounts` quedaba `anon=arwdDxt, authenticated=arwdDxt` y
`has_column_privilege(authenticated, accounts, ig_user_id, UPDATE)` daba **TRUE**.

Lo que hace que no se vea: el gate mide contra un Postgres desechable bootstrapeado a mano, que
**no trae los default privileges de la plataforma**. Los tests de permisos pasan en verde midiendo
un entorno donde el problema no existe. No es un test flojo — es un test que mide otro sistema.

Regla: **un candado de permisos solo está medido si se mide donde la plataforma ya ha concedido
cosas.** Al montar, revocar esos defaults ANTES de aplicar las migraciones, y comprobar el ACL
efectivo (`relacl`, `has_column_privilege`), nunca el texto de la migración.

Ver [[truncate-salta-rls-y-sobrevive-al-revoke-de-update-y-delete]] (misma raíz: los privilegios se
conceden por enumeración y no se quitan por enumeración) · [[una-pieza-con-su-suite-en-verde-que-el-sistema-no-llama]]
