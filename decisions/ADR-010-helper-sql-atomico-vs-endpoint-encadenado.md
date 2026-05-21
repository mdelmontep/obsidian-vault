---
title: ADR-010 — Helper SQL atómico vs endpoint con UPDATEs encadenados para acciones con chain de triggers fiscales
date: 2026-05-21
status: accepted
tags: [adr, facturaia, postgres, conciliacion]
---

## Contexto

Desvincular manualmente una asignación factura↔movimiento (mig 131) requiere: setear `last_revert_at` ANTES del UPDATE mfa para que el chain `recompute → mirror → auto_mark_*` corra con guard activo. Si no, loop infinito + bug fiscal reentra (commit `9631638`).

## Opciones consideradas

- **A — SQL function `desvincular_asignacion()` invocada por RPC**: UPDATE facturas + UPDATE mfa + INSERT module_event en una sola transacción, FOR UPDATE lock, idempotente.
- **B — 3 UPDATEs encadenados desde el endpoint TS**: route.ts hace UPDATE 1, UPDATE 2, INSERT 3 con `await admin.from(...)` secuenciales.
- **C — Sin orden explícito, confiar en trigger `auto_mark_*` para no re-casar**: trivial pero incorrecto (verificado: loop).

## Decisión

**A**, porque B no garantiza orden cross-statement (Supabase JS no expone transacción multi-statement) y el chain de triggers requiere que `last_revert_at` esté visible al momento exacto del UPDATE mfa. SQL function + RPC garantiza atomicidad + lock + audit en un solo round-trip.

## Consecuencias

- Cada acción manual fiscal con chain de triggers debe envolverse en SQL function similar (precedente). Aplica a confirm-sugerencia con force (PR #69 lo respetó usando SET `last_revert_at=NULL` explícito).
- Tests pasan a ser SQL-level + endpoint contract test, no solo unit.
- Comentario crítico en la función documenta el orden — refactores futuros leen rationale en código, no en PRs.
