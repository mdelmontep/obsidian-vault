---
title: extender un unique de idempotencia con columna nullable usando NULLS NOT DISTINCT
date: 2026-06-16
source: claude-code-session
tags: [postgres, idempotencia, supabase, schema]
---

Para añadir una dimensión OPT-IN a un índice único de idempotencia sin romper las
filas viejas (que la tienen NULL): recrea el índice incluyendo la nueva columna con
`NULLS NOT DISTINCT` (PG15+).

Caso (mig 308 stock): el ledger era idempotente por `(documento_id, catalogo_id, tipo)`.
Al añadir lotes pasa a `(documento_id, catalogo_id, tipo, lote_id) NULLS NOT DISTINCT`:

- Sin lote (`lote_id` NULL): NULLS NOT DISTINCT trata los NULL como iguales →
  idempotencia idéntica a antes (una fila por doc/producto/tipo). El camino sin
  lotes no cambia de comportamiento.
- Con lote: distintos `lote_id` del mismo doc/producto/tipo son válidos (una venta
  puede salir de N partidas del mismo producto).

Sin `NULLS NOT DISTINCT`, Postgres trata cada NULL como distinto → se duplicarían
los movimientos de las filas sin lote (se rompe la idempotencia existente).

Ver [[unique-index-concurrently-parcial-para-idempotencia-bd]].
