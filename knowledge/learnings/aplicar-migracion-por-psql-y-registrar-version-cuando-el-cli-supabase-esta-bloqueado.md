---
title: aplicar migración por psql + registrar versión cuando el CLI de Supabase está bloqueado
date: 2026-07-19
source: claude-code-session
tags: [supabase, migraciones, red, psql]
---
Desde redes que bloquean los puertos Postgres (5432 / pooler 6543), `supabase
db push --linked` y `migration repair` CUELGAN — pero un `psql
"$SUPABASE_DB_URL" ...` directo SÍ conecta (usa otra ruta). Workaround para
aplicar una migración YA commiteada sin dejar huérfano:

1. `psql "$SUPABASE_DB_URL" -v ON_ERROR_STOP=1 -f supabase/migrations/NNN_x.sql`
2. Registrar la versión (equivalente a `migration repair --status applied`):
   `insert into supabase_migrations.schema_migrations (version,name)
    values ('NNN','x') on conflict (version) do nothing;`
   (columnas: version text, statements text[] nullable, name — con name basta.)

Mantén el formato **NNN** (no timestamp): el hook pre-push aborta si detecta
timestamps en el remote, y esta tabla ya viene en NNN. Verifica después:
`select proname from pg_proc where ...` + versión en `schema_migrations`.
Solo para migraciones additivas/`create or replace` (reversibles). No es
sustituto de `db push` cuando la red no está bloqueada.
Relacionado: la deuda "reconciliar migs timestamp" del hub venía de aplicar por
MCP (que grababa timestamp) — este método evita eso.
