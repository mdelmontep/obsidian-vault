---
title: verificar check constraint en prod con count exacto rest (sin tocar filas)
date: 2026-05-22
source: claude-code-session
tags: [supabase, postgrest, smoke, postgres]
---

Para validar que un CHECK constraint cumple su invariante en prod sin hacer UPDATE/INSERT real: query REST con la **negación** del invariante + `Prefer: count=exact` + `Range: 0-0` → `content-range: */0` confirma 0 violaciones.

Patrón: si el CHECK dice `(A AND B) OR (NOT A AND NOT B)`, la negación es `(A AND NOT B) OR (NOT A AND B)` → filtro PostgREST `or=(and(...),and(...))`.

Caso 2026-05-22 FacturaIA mig 126 `revoked_at ⟺ estado`:
`or=(and(revoked_at.not.is.null,estado.not.in.(revocado,expirado)),and(revoked_at.is.null,estado.in.(revocado,expirado)))` → `*/0`.

Combina con leer DDL del `.sql` para certeza total. Respeta regla "smoke con IDs garantizadamente fuera de rango" — no toca ninguna fila real. Alternativa para test runtime activo (INSERT/UPDATE) requiere row sintético con UUID nuevo + verificar que el INSERT falla.
