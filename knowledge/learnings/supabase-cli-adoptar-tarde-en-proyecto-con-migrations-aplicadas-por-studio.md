---
title: adoptar supabase CLI en proyecto con migrations aplicadas a mano por Studio
date: 2026-05-20
source: claude-code-session
tags: [supabase, migrations, cli, onboarding]
---

Si el equipo lleva pegando SQL en Studio, `supabase_migrations.schema_migrations` solo trackea las primeras (las que sí pasaron por CLI). El resto está en BD pero el CLI las ve como pendientes → `db push` intenta re-aplicar todo → conflictos.

Pasos:
1. `brew install supabase/tap/supabase` + `supabase login` (Terminal real, no Claude Code: no es TTY).
2. `supabase link --project-ref <ref>` desde la raíz del repo.
3. `supabase migration list --linked` → ver qué tiene Remote vacío.
4. **Probes SQL** contra prod para confirmar qué migs están aplicadas — NO fiar del changelog/hub:
   ```sql
   SELECT EXISTS(SELECT 1 FROM pg_proc WHERE proname='<func_de_la_mig>');
   ```
5. `supabase migration repair --linked --status applied <v1> <v2> ...` (solo metadata, no re-ejecuta SQL — cero riesgo).
6. Verificación final: `supabase db push --dry-run --linked` ⇒ "Remote database is up to date".

[[supabase-cli-skipea-migrations-con-prefijo-no-puramente-numerico]]
