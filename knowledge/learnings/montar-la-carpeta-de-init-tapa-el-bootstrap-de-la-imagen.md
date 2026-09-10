---
title: montar la carpeta de init entera tapa el bootstrap que trae la imagen
date: 2026-09-10
source: mandadm
tags: [docker, postgres, supabase, volumenes]
---
`- /opt/x/init:/docker-entrypoint-initdb.d:ro` no **añade** scripts de arranque: **sustituye** el
directorio. En `supabase/postgres` ahí viven `init-scripts/`, `migrate.sh` y `migrations/`, que son
quienes crean los roles `anon`/`authenticated`/`service_role` y el esquema `auth`. Taparlos deja una
base sin nada de eso — y las FK a `auth.users` y `auth.uid()` de las migraciones de la app no tienen
dónde agarrarse.

Fix: montar el **fichero suelto**, no la carpeta:
`- /opt/x/init/zz-mio.sh:/docker-entrypoint-initdb.d/zz-mio.sh:ro`

El prefijo importa: el entrypoint recorre el directorio en orden alfabético, así que `zz-` corre
**después** del bootstrap de la imagen y `99-` correría **antes** (los dígitos van delante de las
letras en ASCII). Y que sea `.sh` y no `.sql` si necesita variables de entorno: los `.sql` se pasan
por `psql -f`, sin sustitución.

Aplica a cualquier imagen con directorio de init (postgres, mysql, mongo), no solo a Supabase.
