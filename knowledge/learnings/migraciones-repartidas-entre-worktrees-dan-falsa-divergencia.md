---
title: dos worktrees con migraciones distintas hacen que el cli de supabase vea divergencia
date: 2026-07-29
source: claude-code-session
tags: [supabase, git-worktree, migraciones]
---
Trabajando dos PRs en paralelo (un worktree por PR), cada uno tiene solo SU migración.
El CLI compara la carpeta local contra `schema_migrations` del remoto, así que en cuanto
aplicas la del worktree A, el worktree B ve una versión remota que él no tiene y aborta
el `db push` pidiendo `migration repair` / `db pull`. No hay nada roto: es que ningún
worktree tiene la foto completa.

Dos cosas que ahorran la pelea:

- El link del proyecto vive en `supabase/.temp/` y está gitignored, así que un worktree
  nuevo NO está linkeado (`Cannot find project ref`). `cp -r` esa carpeta del checkout
  principal, o exporta los comandos desde él. Copiarla **no basta**: la credencial del
  login role no vive ahí, así que `mig:renumerar` y `db push` piden además
  `SUPABASE_DB_PASSWORD=...` en la misma línea o fallan con `password authentication
  failed for user "cli_login_postgres"`.
- **Y hay que borrarla al terminar** (10-sep-2026): mientras esos ficheros están, el
  `gen:types:check` del `pre-push` deja de comparar contra el fichero del repo y compara
  contra PROD, así que un worktree que solo quería empujar código empieza a rebotar por una
  deriva de tipos que no es suya.
- Para empujar, copia temporalmente al mismo worktree las migraciones ya aplicadas que
  le falten, haz el `db push`, y bórralas. Vuelven solas con el merge/rebase.

Mejor aún: numerar y aplicar en serie (mergear el PR-1 antes de aplicar la migración del
PR-2), que además evita colisiones de número. Caso real: TuFacturaIA migs 583-587 con
dos worktrees, 28-jul.
