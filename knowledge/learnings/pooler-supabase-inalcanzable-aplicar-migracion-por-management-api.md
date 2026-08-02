---
title: pooler de supabase inalcanzable — migrar por management api y registrar la versión a mano
date: 2026-08-02
source: claude-code-session
tags: [supabase, migraciones, red]
---
Hay redes donde el pooler de Supabase no responde (5432 y 6543 dan timeout) aunque el proyecto esté
`ACTIVE_HEALTHY`: `db push` es inservible. La Management API sí va, porque es HTTPS:
`POST /v1/projects/{ref}/database/query` con el token del CLI (llavero de macOS, `security
find-generic-password -s "Supabase CLI" -w`).

Pero ejecutar el SQL **no basta**: `db push` además registra la versión. Sin ese registro el cambio es
huérfano y el siguiente push lo reaplica o lo da por hecho y se salta el siguiente. Hay que insertarlo:

```sql
create schema if not exists supabase_migrations;
create table if not exists supabase_migrations.schema_migrations (version text primary key, statements text[], name text);
insert into supabase_migrations.schema_migrations (version, name) values ('001','core') on conflict do nothing;
```
Ver [[supabase-migration-numero-colision-renumerar]].
