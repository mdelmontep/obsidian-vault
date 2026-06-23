---
name: supabase-cli-db-push-fail-por-historico-desincronizado-workaround
description: db push falla si remoto tiene timestamps sin archivo local. Workaround quirúrgico — db query -f + migration repair selectivo.
date: 2026-05-22
source: claude-code-session
tags: [supabase, migrations, cli, deploy]
---

**Síntoma**: `supabase db push --linked` aborta con `"Remote migration versions not found in local migrations directory"` listando timestamps tipo `20260521113946` que no tienen archivo `supabase/migrations/<timestamp>_*.sql` en el repo. Típico tras: `db pull` antiguo, cambios SQL vía Supabase Studio sin commit, o trabajos paralelos en branches.

**Workaround quirúrgico** (no requiere borrar histórico remoto):
1. Aplicar las migs locales pendientes una a una con `supabase db query --linked -f supabase/migrations/146_xxx.sql`. Ejecuta el SQL directo sin tocar el histórico.
2. Tras aplicar, sincronizar el histórico con `supabase migration repair --linked --status applied 146 147 148 149 150`. Solo marca en `supabase_migrations.schema_migrations` que esas versiones se aplicaron — NO re-ejecuta SQL.
3. Las versiones remotas "fantasma" (timestamps sin archivo local) **se quedan**. No estorban si no intentas `db push` posterior. Si quieres limpiarlas: `--status reverted <timestamp>` solo funciona si existe archivo local con ese timestamp.

**Verificar** post-fix: `supabase migration list --linked` muestra las 146-150 con check en columna remoto.

Caso real TuFacturaIA 2026-05-22: 13 timestamps remotos huérfanos bloqueaban deploy migs 146-150. Aplicación quirúrgica + repair selectivo desbloqueó deploy en 5 minutos sin tocar `supabase_migrations.schema_migrations` manualmente.

**Variante (2026-06-23): el huérfano es una migración LEGÍTIMA aplicada desde una rama sin mergear.** Si el `NNN` remoto-sin-local corresponde a una migración real que alguien aplicó a prod desde una feature branch que aún no está en main (no es basura de Studio), el fix correcto NO es `repair --status reverted` (mentiría: marca "no aplicado" algo vivo —p.ej. un trigger de compliance VeriFACTU—) ni `db pull` (genera timestamp, rompe NNN). Es: **traer SOLO ese archivo de migración a main** (`git checkout <rama> -- supabase/migrations/NNN_*.sql` + commit), sin arrastrar el resto de la feature branch. El repo pasa a reflejar prod, `db push --dry-run` confirma que solo queda lo nuevo, y `db push --yes` aplica. Caso real: mig 376 (guard inalterabilidad VeriFACTU) bloqueaba aplicar la 378; traer solo la 376 a main lo desbloqueó. Regla: identifica QUÉ es el huérfano (`git log --all -S` / `--diff-filter=A`) antes de elegir repair vs traer-archivo.
