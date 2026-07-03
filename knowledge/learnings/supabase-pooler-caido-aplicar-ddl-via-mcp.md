---
title: pooler supabase caído (5432 timeout) → aplicar ddl vía mcp execute_sql
date: 2026-07-03
source: claude-code-session
tags: [supabase, migraciones, infra]
---
Si `supabase db push`/`psql` cuelgan con "timeout expired" al pooler
(`aws-*.pooler.supabase.com:5432`), es caída transitoria del pooler — la API
de gestión (HTTPS) sigue viva. Fallback para no bloquear la sesión:

- Aplicar el DDL idempotente (`add column if not exists`, `create ... if not
  exists`) vía MCP `supabase execute_sql` (verifica antes `get_project_url` ==
  el ref de `.env.local`).
- `gen:types` funciona igual (usa management API, no el pooler).
- El cliente de la app (`createAdminClient`, PostgREST HTTPS) también sigue
  funcionando → los verify scripts corren.

Deuda: las columnas quedan en prod pero SIN registrar en
`supabase_migrations.schema_migrations`. Cuando el pooler recupere, correr
`supabase db push` (re-ejecuta la migración como no-op por `IF NOT EXISTS` y la
registra) para no dejar huérfana. Ver [[gen-types-linked-no-db-url]].
