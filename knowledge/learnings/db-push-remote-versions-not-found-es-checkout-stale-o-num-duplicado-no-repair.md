---
title: "supabase db push 'remote versions not found in local' = checkout stale o nº migración duplicado, NO migration repair"
date: 2026-07-21
source: claude-code-session
tags: [supabase, migraciones, db-push]
---
`supabase db push` aborta con "Remote migration versions not found in local migrations directory" y SUGIERE `migration repair --status reverted <NNN>`. **NO lo corras**: marcar como reverted migraciones que SÍ están bien aplicadas en prod corrompe el historial de la BD.

Causas reales (ninguna necesita repair):
1. El checkout desde el que lanzas está DESACTUALIZADO (le faltan ficheros `NNN_*` que ya están en main+prod). Fix: `git fetch` + checkout de la rama con todas las migs, reintenta. Ojo: no puedes `checkout` una rama ya usada por otro worktree → lanza el push desde ese worktree.
2. Nº de migración DUPLICADO en el repo (dos `NNN_*.sql`): rompe el push para todo el equipo. Detecta: `git ls-files supabase/migrations | grep -oE '/[0-9]{3}_' | sort | uniq -d`. Si un fichero es huérfano idéntico a otro con su nº real (difieren solo en la cabecera), bórralo — el contenido se conserva en el real.

**3ª causa, 20-ago-2026: el fichero NUNCA se commiteó.** Prod tenía aplicadas la 726 y la 727 y en `origin/main` solo existía la 727: la 726 vivía SUELTA y sin trackear en el worktree de otra sesión. Aquí ningún `fetch` ni cambio de rama arregla nada —no es checkout stale— y `db push` queda roto **para todas las sesiones** hasta que ese fichero aterrice en main. Detecta el caso con `supabase migration list --linked`: la fila sale con `local = —` y `remote = NNN`. Y ojo con renumerar para salir del paso: el script mira lo aplicado en prod, así que tu propio número te sale ocupado por ti mismo, y si lo mueves el registro de prod se queda mintiendo.

**19-ago-2026, misma trampa con otro nombre**: desde un worktree por detrás de main el CLI aborta con `LegacyDbPushMissingLocalError` y propone `migration repair --status reverted 714 715 … 721` — ocho migraciones de OTRA sesión, aplicadas y correctas. Es la causa 1 (checkout stale) con el error renombrado. Salida usada: `psql -v ON_ERROR_STOP=1 -f <mig>` y registrar la fila de la versión a mano. Regla: si el `repair` que te proponen menciona números que no son tuyos, la orden está mal, no la base.

Verifica siempre con `--dry-run` que el plan sean solo tus migs nuevas antes del push real. Aplica con `--db-url "$SUPABASE_DB_URL"` (de `.env.local`) desde un worktree con las migs si `--linked` no encaja. NUNCA `apply_migration` del MCP (graba versión timestamp → rompe el hook pre-push). Caso real: dup `519` (orphan obras_materiales_trazabilidad_ia, real en 524) bloqueaba el push de Fase 2 Obras multi-presupuesto.
Relacionado: [[aplicar-migracion-por-psql-y-registrar-version-cuando-el-cli-supabase-esta-bloqueado]] · [[facturaia]]
