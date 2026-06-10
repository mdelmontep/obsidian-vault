---
title: Worktree en facturaia — node_modules real para next build + copiar link Supabase
date: 2026-06-10
source: sesión fiscal etapa 2 (worktree feat/fiscal-etapa2-captura)
tags: [worktree, nextjs, turbopack, supabase, facturaia, workflow]
---

Al trabajar en un `git worktree` aislado de **facturaia** (patrón habitual para PRs sin arrastrar commits locales):

- **`node_modules` symlinkado al repo principal sirve para `typecheck` y `vitest`, pero ROMPE `next build`**: Turbopack falla con `Symlink [project]/node_modules is invalid, it points out of the filesystem root`. Fix: `rm node_modules && npm ci` (real) en el worktree. Coste único; los builds siguientes lo reutilizan.
- **El link de Supabase NO está en el worktree**: vive en `supabase/.temp/` del repo principal (gitignored). Sin él, `supabase db push`/`migration list --linked` fallan con `Cannot find project ref`. Fix: `cp -r <repo-principal>/supabase/.temp <worktree>/supabase/.temp`.
- `.env.local` también es gitignored → symlinkarlo o copiarlo si el worktree lo necesita.

Secuencia de aplicar migraciones desde worktree: `migration list --linked` (confirmar que solo aparecen las tuyas como pendientes — otra sesión puede haber mergeado migraciones intermedias) → `db push --linked` → verificar el schema real en prod por psql antes de mergear el PR.
