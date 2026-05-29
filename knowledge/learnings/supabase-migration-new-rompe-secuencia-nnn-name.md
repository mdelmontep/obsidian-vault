---
title: supabase migration new rompe formato NNN_name.sql → registry queda con timestamp huérfano
date: 2026-05-29
source: claude-code-session
tags: [supabase, migrations, ops]
---

Si el proyecto usa convención `NNN_name.sql` (números secuenciales), `supabase migration new` genera `<timestamp>_name.sql` y al aplicar deja la fila en `supabase_migrations.schema_migrations` con `version='20260528185823'` (timestamp), no con `version='NNN'`. Resultado: `supabase migration list --linked` muestra registro huérfano que `db push` no sabe matchear.

Patrón paralelo: SQL aplicado a mano (Dashboard SQL Editor, psql directo) **no genera fila** en `schema_migrations` → check físico de información_schema dice que columnas/funciones existen, pero CLI las considera pendientes y un `db push` limpio intentaría reaplicarlas.

Reconciliación correcta:
1. `supabase migration repair --status reverted <timestamp>` — elimina la fila huérfana.
2. `supabase migration repair --status applied <NNN>` — registra la mig canónica.
3. Repetir para todas. Solo después `db push --linked` aplicará lo pendiente real.

NO usar `supabase db pull` para reconciliar — genera nueva mig que captura el remote y crea más diff.

Hook git pre-push (`.githooks/pre-push`) que detecte timestamps >12 dígitos en `migration list --linked` previene volver a entrar en este lío. Auto-install via `npm prepare` script: `git config core.hooksPath .githooks`. Ver TuFacturaIA `.githooks/pre-push` (sesión 2026-05-29).
