---
title: migración aplicada fuera de `supabase db push` no entra en schema_migrations → reaplicar falla
date: 2026-05-27
source: claude-code-session
tags: [supabase, postgres]
---

Aplicar una migración por `psql -f` o por el MCP `apply_migration` NO la registra en `supabase_migrations.schema_migrations` con el `NNN` del repo (psql no la registra en absoluto; el MCP la registra con timestamp `20260527…`, no `173`).

Consecuencia: un futuro `supabase db push` la considera pendiente y la **reaplica** → revienta en lo no idempotente (`ADD CONSTRAINT`, `CREATE TYPE`, `ADD COLUMN` sin IF NOT EXISTS).

Fix doble:
- **Idempotencia en el archivo del repo**: `CREATE TABLE/INDEX IF NOT EXISTS`, `ADD COLUMN IF NOT EXISTS`, y para constraints `ALTER … DROP CONSTRAINT IF EXISTS x; ALTER … ADD CONSTRAINT x …`. Así reaplicar = no-op seguro.
- **Reconciliar historial**: `UPDATE supabase_migrations.schema_migrations SET version='NNN' WHERE version='<timestamp>'`, o insertar la fila si falta.

Caso real 2026-05-27 (TuFacturaIA): migs 172/173 aplicadas out-of-band → quedaron fuera del historial. Ver [[reference-supabase-db-access]].

Caso real 2026-06-19 (migs 339/340/341): CLI da `i/o timeout` por pooler → usar MCP `apply_migration`. El MCP ejecuta el SQL pero registra con timestamp en lugar de `NNN`. Fix: INSERT manual en `supabase_migrations.schema_migrations` con `version='339'` y `statements=ARRAY['-- placeholder']`.
