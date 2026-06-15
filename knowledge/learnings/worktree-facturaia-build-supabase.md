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
- **Sesión paralela en el MISMO dir principal = colisión**: comparten HEAD/índice de git → tu `commit` puede caer en la rama de la otra sesión y pushearse con ella (caso real 2026-06-11: mi commit de bandeja acabó en su `fix/llm-robustez`). Si detectas otra sesión activa (ficheros ajenos en `git status`, checkouts recientes en `reflog`), trabaja en worktree desde el inicio. Recuperar la rama ajena: `git push --force-with-lease` a su estado anterior.

Secuencia de aplicar migraciones desde worktree: `migration list --linked` (confirmar que solo aparecen las tuyas como pendientes — otra sesión puede haber mergeado migraciones intermedias) → `db push --linked` → verificar el schema real en prod por psql antes de mergear el PR.

- **Trinquete de inline-styles desincronizado por sesión paralela**: el pre-commit (`scripts/inline-style-ratchet.mjs` vs `.inline-style-baseline.json`) **bloquea tu commit por archivos que no tocaste** si otra sesión mergeó código con inline-styles nuevos sin correr `npm run ratchet:update` (baseline < realidad de `origin/main`). Caso real 2026-06-15: PR de conciliación bloqueado por `inventario-view`/`ficha-producto` de STOCK Fase 2. Fix: deja TUS archivos net-zero (inline → CSS Modules) y corre `npm run ratchet:update`; el diff del baseline solo sube los archivos ajenos ya en main → commitéalo documentando que es deuda pre-existente sincronizada, no introducida por tu PR. NO uses `--no-verify` (saltaría también build).
