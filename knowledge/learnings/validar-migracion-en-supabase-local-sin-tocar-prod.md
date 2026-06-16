---
title: validar una migración sin mergear en stack supabase local (no prod)
date: 2026-06-16
source: claude-code-session
tags: [supabase, migracion, postgres, workflow, facturaia]
---

Para validar el SQL de una migración antes de mergear, sin aplicarla a prod
(inviolable: `db push` a prod deja timestamp huérfano + drift):

- Si el repo no tiene `supabase/config.toml` (modo solo-migraciones-linkeadas) →
  `supabase init` lo genera (PG17 por defecto). Es untracked; bórralo antes de commitear.
- Si YA hay otro stack local corriendo (otra sesión/worktree) colisiona en el
  puerto 54322. Cambia los puertos del config (54321/54322/54320/54323/54324/54327
  → 544xx) y arranca con `supabase start -x studio,storage-api,realtime,...`
  (excluye servicios pesados; solo necesitas `db` para el reset).
- `supabase db reset --local` reproduce 001→N: valida sintaxis, refs, constraints,
  `NULLS NOT DISTINCT`, ON CONFLICT con índice de expresión, cuerpos de funciones.
- Smoke funcional con psql: inserta fixtures con `set session_replication_role = replica`
  (salta triggers de huella/stock/FK), vuelve a `origin` y llama a la función bajo
  prueba; `\set ON_ERROR_ROLLBACK on` para testear errores esperados (unique, raise);
  `rollback` al final (DB desechable). `supabase stop` al terminar.

Ver [[worktree-facturaia-build-supabase]] (build/push real desde worktree).
