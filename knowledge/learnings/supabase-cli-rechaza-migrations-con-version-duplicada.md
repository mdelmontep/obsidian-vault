---
title: supabase CLI rechaza migrations con versión duplicada
date: 2026-05-07
source: claude-code-session
tags: [supabase, migrations, ci]
---

Dos archivos con el mismo prefijo numérico (`007_a.sql` + `007_b.sql`) hacen que `supabase start` o `db push` falle:

```
ERROR: duplicate key value violates unique constraint "schema_migrations_pkey"
Key (version)=(007) already exists.
```

Detectar antes de commit:

```bash
ls supabase/migrations/ | grep -oE '^[0-9]+' | sort | uniq -d
```

Fix: escoger el archivo con SQL más idempotente (`IF NOT EXISTS`, `ON CONFLICT DO NOTHING`, `COMMENT`) y renombrarlo al primer slot libre tras max actual. NO el que tenga `UPDATE`/`DELETE` destructivos (re-aplicar duplica datos).

Producción no se rompe si SQL idempotente — pero CI con `supabase start` arrancando desde cero sí.

**Variante latente (caso 2026-05-30 TuFacturaIA)**: el 2º archivo duplicado puede estar *aplicado en prod pero fuera del ledger* (sus objetos existen; `schema_migrations` solo registró el 1º). Entonces `db push` se bloquea con *"Found local migration files to be inserted before the last migration"* y pide `--include-all` (que reintenta insertar la versión duplicada → conflicto). **`migration repair --status applied N` NO lo arregla.** Fix real: renombrar el idempotente al slot libre (`190_x`→`192_x`), `db push --dry-run` para confirmar, y el re-push lo aplica como no-op registrando la versión nueva → ledger reconciliado.
