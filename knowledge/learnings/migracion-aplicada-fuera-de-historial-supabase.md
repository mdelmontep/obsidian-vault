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

**El timeout del pooler suele ser TRANSITORIO** (red del sandbox de Claude Code, no caída de Supabase). Antes de recurrir al MCP+INSERT manual (que genera justo el timestamp huérfano de arriba), **reintenta `supabase db push --linked`**; para LEER/verificar prod el MCP (HTTPS :443) sí llega aunque el pooler `:5432` dé timeout. Caso real 2026-06-24 (migs 383/384, TuFacturaIA): `db push` limpio en cuanto se desbloqueó la red → version `383`/`384` correcta, 0 huérfanos.

**Efecto nuevo descubierto 2026-07-25 (TuFacturaIA)**: un timestamp huérfano no solo se reaplica, además **desalinea `supabase migration list` a partir de esa versión**. El CLI empareja local/remoto como merge de dos listas ordenadas por version-como-string, y `'20260723…'` cae entre `'202'` y `'203'`: desde ahí TODO sale desparejado (353 migraciones "pendientes" que en realidad estaban aplicadas). Un `db push` a ciegas en ese estado es catastrófico.

Fix canónico, sin tocar la tabla a mano: `supabase migration repair --status applied <NNN>` para la que ya está aplicada de facto y `--status reverted <timestamp>` para retirar el huérfano. Tras eso, `migration list` sin desparejados. Y verificar SIEMPRE el estado **de facto** (¿existe la función/columna que crea?) antes de decidir applied vs reverted. Caso real: 2 huérfanos del 2026-07-23; uno era la mig 552 del repo, el otro una función (`editar_importe_asignacion`) **que no existía en ningún fichero** → hubo que recuperarla al repo desde `schema_migrations.statements`.
