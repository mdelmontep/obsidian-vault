---
title: create or replace view falla tras add column si la view usa f.*
date: 2026-05-05
source: claude-code-session
tags: [supabase, postgres, views, migrations]
---

Al añadir columnas a una tabla base con `ALTER TABLE` y luego hacer `CREATE OR REPLACE VIEW` sobre una vista que la consume con `SELECT f.*, ...`, Postgres rompe con `ERROR 42P16: cannot change name of view column "X" to "Y"`.

Causa: `*` se expande en orden posicional. Las columnas nuevas de la tabla cambian el shape; CREATE OR REPLACE exige nombre+orden idénticos.

Fix: `DROP VIEW IF EXISTS X` antes de `CREATE VIEW X`. Tras `CREATE`, reaplicar `ALTER VIEW X SET (security_invoker = true)` (Postgres 15+) — sin esto la vista bypassea RLS del caller.

Caso real FacturaIA migration 039: añadí `created_by_actor_email/name` a `facturas` y `presupuestos`, vistas `*_con_autor` con `f.*` rompieron en CREATE OR REPLACE. Cambio a DROP+CREATE en mismo migration: limpio.
