---
title: schema_migrations no es source of truth si aplicas manual
date: 2026-05-07
source: claude-code-session
tags: [supabase, migrations, deploy]
---

Si las migraciones en producción se aplican vía Dashboard SQL (no `supabase db push --linked`), la tabla `supabase_migrations.schema_migrations` queda incompleta. Caso real: 49 archivos en repo, 8 entradas en prod.

Para verificar qué hay aplicado, NO consultar `list_migrations` ni la tabla. Consultar el contenido directo:

```sql
SELECT 1 FROM information_schema.columns WHERE table_name='X' AND column_name='Y';
SELECT 1 FROM pg_trigger WHERE tgname='Z';
SELECT relrowsecurity FROM pg_class WHERE relname='T';
```

Implicación: re-aplicar una migration idempotente (IF NOT EXISTS / ON CONFLICT) en prod es no-op aunque schema_migrations no la trackee. La tabla solo es fiable si todo el equipo aplica vía CLI.

**Escape cuando `supabase db push` falla por drift**: `supabase db query --linked -f <file.sql>` ejecuta SQL directo contra remoto sin tocar el tracking. Útil cuando los timestamps remote (formato `YYYYMMDDHHMMSS` aplicados via Studio) no coinciden con los nombres locales `NNN_*.sql` y `db push --dry-run` rechaza por "Remote migration versions not found in local". Caso real TuFacturaIA 2026-05-21: aplicar mig 142 con 13 migs remote no trackeadas; `db query --linked -f` la ejecutó limpia (transacción + assert pasaron) sin necesidad de `migration repair` previo.
