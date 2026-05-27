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

Caso real 2026-05-27 (TuFacturaIA): migs 172/173 aplicadas out-of-band (op + CLI sin token; psql con password rotada) → quedaron fuera del historial. Ver [[reference-supabase-db-access]] para la vía fiable (MCP OAuth).
