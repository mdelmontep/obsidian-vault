---
title: supabase migration número colisión entre ramas — renumerar
date: 2026-06-30
source: claude-code-session
tags: [supabase, migrations, git]
---

**Síntoma**: `supabase db push --linked` dice "Remote database is up to date" pero la columna no existe. La migración NNN local colisiona con una NNN remota de otra rama ya mergeada.

**Por qué**: `schema_migrations` registra versiones por número. Si la rama A mergea `418_foo` antes que la rama B, el `418_bar` de B queda "marcado como aplicado" sin ejecutarse nunca.

**Fix**:
1. `git mv NNN_nuevo.sql NNN+1_nuevo.sql` + actualizar cabecera `-- NNN_` en el archivo
2. Crear placeholder `NNN_nombre-real.sql` (solo comentario) para la migración remota huérfana
3. `supabase migration repair --status applied NNN --linked`
4. `supabase db push --linked` → aplica `NNN+1`
5. Commit: `git add` ambos archivos + push

**Prevenir**: asignar el número al ABRIR el PR, no al crear la rama. Verificar con `ls supabase/migrations | tail -1` justo antes de abrir.
