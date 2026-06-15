---
title: proyección denormalizada de un ledger diverge en silencio sin un detector
date: 2026-06-15
source: claude-code-session
tags: [supabase, integridad, ledger, observabilidad]
---
`stock_actual` (proyección) vs `stock_movimientos` (ledger = fuente de verdad).
Todos los flujos de la app los mantienen atómicos (movimiento + proyección en
el mismo bloque RPC/trigger). Pero NADA impide que un UPDATE directo en BD, un
fallo externo o una migración desincronicen la proyección — y un `recompute`
la "arregla" en silencio, ocultando que hubo drift. El valor derivado (p.ej.
valoración de inventario) miente sin que nadie se entere.

Patrón: para toda proyección de un ledger, enviar un **detector de drift**
(`SELECT … GROUP BY id HAVING proyección <> Σ(ledger)`) + una superficie de
reconciliación visible (banner/endpoint con audit), no solo el recompute mudo.
Misma familia que [[agregado-cacheado-sobre-ledger-recompute-trigger]].
Caso: TuFacturaIA mig 295 `detect_stock_drift` + `/api/stock/drift` (PR #262).
