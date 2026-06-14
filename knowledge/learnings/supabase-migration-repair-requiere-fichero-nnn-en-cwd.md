---
title: supabase migration repair exige que el fichero NNN_*.sql exista en el cwd
date: 2026-06-14
source: claude-code-session
tags: [supabase, migraciones, git, worktree]
---
`supabase migration repair --status applied <N>` falla con
`glob supabase/migrations/<N>_*.sql: file does not exist` si tu checkout va por
detrás del merge que añadió esa migración (el fichero aún no está en disco local,
aunque sí en `origin/main`). El repair lee el fichero del cwd, no del remoto.

Fix: reparar desde un **worktree de `origin/main`** (que sí tiene el fichero), o
`git pull` antes. Caso 2026-06-14 (TuFacturaIA): el checkout principal seguía en
`main` viejo; `repair 279 280` aplicó 279 pero falló en 280 hasta hacerlo desde un
worktree detached de origin/main.

Relacionado: [[supabase-db-push-colision-numeracion-migraciones-rama-stale]],
[[migracion-aplicada-fuera-de-historial-supabase]].
