---
title: ningún gate de texto ve un create policy contra una columna que no existe
date: 2026-08-02
source: claude-code-session
tags: [postgres, supabase, migraciones, gates, docker, tucrmia]
---
Los gates que comparan ficheros del repo contra ficheros del repo no pueden decir si el SQL es válido:
comparan el repositorio consigo mismo. Un `create policy` contra una columna inexistente pasa los tres
gates y revienta al aplicar.

Fix barato y sin red: replay contra un `postgres:17-alpine` desechable. Un `00_bootstrap.sql` con los tres
roles de Supabase, el esquema `auth`, `auth.users` y `auth.uid()` leyendo `request.jwt.claims`; después
todas las migraciones con `ON_ERROR_STOP=1`. No necesita token ni el proyecto de producción.

Lo que desbloquea, y es lo que lo hace rentable:
- afirmaciones de aislamiento EJECUTADAS: sembrar dos orgs y comprobar que no se ve la ajena. Corrido sin
  la migración del arreglo debe fallar — ahí deja de ser un razonamiento
- `has_column_privilege` en vez de parsear grants a mano
- el `EXPLAIN` con volumen: la forma del plan sí se traslada aunque los tiempos no

Dos gotchas: esperar a una consulta real, no a `pg_isready` (durante initdb el servidor temporal responde
que está listo y la base aún no existe); y `pg_jsonschema` no existe fuera de Supabase, se omite y **se
avisa por pantalla** en vez de callarlo.

**Ampliado el 03-ago**: el bootstrap tiene que reproducir también los **privilegios por defecto** del
proveedor. Sin ellos el replay arranca más limpio que producción y es ciego a toda una clase de fallo
—ver [[el-replay-que-arranca-mas-limpio-que-produccion-es-ciego]] y
[[truncate-salta-rls-y-sobrevive-al-revoke-de-update-y-delete]]—.
