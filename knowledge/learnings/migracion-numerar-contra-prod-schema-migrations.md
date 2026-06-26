---
title: Numerar migración contra el repo (no contra prod) → colisión con ramas aplicadas-sin-mergear
date: 2026-06-26
source: TuFacturaIA fix series backfill PR #512 / #514
tags: [supabase, migraciones, db-push, deploy, numeracion, gotcha]
---

## Síntoma

Abrí una migración nueva numerándola `401` mirando `ls supabase/migrations | tail` (repo `main` iba en 399). Pero prod ya tenía aplicadas la `400` y la `401` (`conciliacion`, `mrr_anual_addons`) desde ramas que hicieron `db push` **sin haber mergeado a main todavía**. Mi `401` colisionaba con la `401` ya viva en prod → si la hubiera aplicado, `db push` la habría dado por "ya aplicada" y el backfill **no se habría ejecutado** (bug silencioso); y al mergear la rama de mrr habría dos `401` en el repo.

## Causa raíz

El "primer hueco real" para numerar NO es el `tail` del repo. **Prod (`supabase_migrations.schema_migrations`) puede ir por delante de `main`** cuando hay ramas que aplicaron `db push` a prod pero aún no se mergearon. La fuente de verdad del número siguiente es `max(version)` de prod, no del repo.

## Regla

Antes de numerar una migración: `select max(version::int) from supabase_migrations.schema_migrations;` (vía MCP si el pooler está bloqueado por red). Usar `max(prod, repo) + 1`. Si ya numeraste mal y mergeaste, renumerar con `git mv` + cabecera en un PR de seguimiento (caso: `401→402`).

Relacionado: [[supabase-cli-db-push-fail-por-historico-desincronizado-workaround]] (mismo origen: prod↔main divergen por ramas sin mergear).
