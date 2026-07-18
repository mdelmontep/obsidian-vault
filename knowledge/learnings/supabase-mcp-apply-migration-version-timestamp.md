---
title: MCP supabase apply_migration registra version timestamp, no NNN
date: 2026-07-13
source: FacturaIA — aplicar migs 455/456/457 a prod
tags: [supabase, migraciones, mcp, facturaia, gotcha]
---

# MCP `apply_migration` rompe la convención NNN del repo

Cuando los puertos Postgres están bloqueados (esta red: 5432/6543 timeout → `supabase db push --linked` cuelga), la vía fiable para aplicar una migración a prod es el MCP `mcp__supabase__apply_migration`.

**Gotcha:** aplica el DDL correctamente PERO registra la fila en `supabase_migrations.schema_migrations` con **`version` = timestamp** (`YYYYMMDDHHMMSS`), no con el `NNN` del nombre del fichero. El nombre queda como `NNN_slug` completo. Esto:
- Dispara el hook `pre-push` de FacturaIA (aborta si detecta timestamps en el remote).
- Provoca divergencia en `supabase migration list --linked` (el `NNN` local aparece como no-aplicado).

**Fix (reconciliar, `migration repair` también colgaría por los puertos):** vía MCP `execute_sql`:
```sql
update supabase_migrations.schema_migrations
   set version='NNN', name='slug_sin_prefijo'
 where name='NNN_slug_completo';
```
Verificar después: `select count(*) ... where version ~ '^\d{14}$'` = 0. El `name` en el ledger va SIN el prefijo numérico (como las filas de `db push`). Ver [[supabase-puertos-postgres-bloqueados]].

**⚠️ Seguridad (2026-07-18):** `apply_migration`/`generate_typescript_types` NO aceptan `project_ref` → operan sobre el proyecto que tenga configurado el MCP, que en FacturaIA es **PROD** (`list_migrations` devuelve las 500+ migs de prod; `list_branches` falla con `Project reference is missing`). Es decir: NO se puede usar este MCP para aplicar a una rama de dev — un `apply_migration` con un `DROP COLUMN` iría directo a prod. Antes de aplicar cualquier DDL por MCP, confirma con `list_migrations` que estás donde crees. Para trabajo que necesita rama de dev sin tocar prod: `db push` desde main limpio (lo aplica el humano) o arreglar el `project_ref` de ramas del MCP.
