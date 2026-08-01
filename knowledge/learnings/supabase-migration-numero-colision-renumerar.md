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

**Prevenir**: asignar el número justo antes del **MERGE** — no al crear la rama ni al abrir el PR: mientras el PR espera, otro se lleva el hueco. Y con script, no a ojo (en TuFacturaIA, `npm run mig:renumerar`).

**El destino es máximo+1, NO el primer hueco** (2026-08-01): los huecos de la secuencia suelen estar **reservados por PRs abiertos sin mergear**, así que ir al primero te manda justo a la colisión que querías evitar. Ese día faltaban el 603 y el 605 en `main` y los tenía un PR pendiente.

**Y cuidado con que el script se cuente a sí mismo**: el de TuFacturaIA metía `git ls-files` —que incluye la migración nueva de la rama— en el conjunto de ocupados, así que con main en 606 y una local 607 proponía el 608, y cada pase volvía a empujar (608 → 609…). De ahí venía la regla «córrelo UNA sola vez»: un parche de memoria humana sobre un off-by-one. Arreglado excluyendo las migraciones de la propia rama → idempotente. **Si una herramienta trae una regla de uso del tipo «no lo corras dos veces», sospecha de la herramienta antes que de tu memoria.**
