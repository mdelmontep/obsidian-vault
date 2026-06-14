---
title: agregado cacheado sobre tabla-ledger compartida → recompute por trigger, no a mano en el rpc
date: 2026-06-14
source: claude-code-session
tags: [postgres, arquitectura, conciliacion]
---
Si una feature crea filas en una tabla-ledger COMPARTIDA (p.ej.
`movimiento_factura_asignacion`) y cachea un agregado en su propia entidad
(`anticipo.importe_aplicado`, `factura.estado`), el RPC del happy-path NO basta
para mantenerlo: cualquier OTRO camino que mute el ledger lo deja stale.

- Caso TuFacturaIA: `aplicar_anticipo` cacheaba `importe_aplicado` incrementándolo a mano. `desvincular_asignacion` (que no conocía `anticipo`) borraba la mfa → saldo congelado → anticipo irrecuperable. Lo encontró un agente "completeness critic" en la 2ª auditoría.
- Fix: trigger `AFTER INSERT OR UPDATE OF <flag> ON <ledger>` que recomputa el agregado desde `Σ(activas)` y lo escribe en la entidad. Mismo patrón que `recompute_factura_estado`. El RPC deja de mantenerlo a mano y lo relee para el retorno.
- NO es el "sync col↔col por trigger" prohibido: es una **proyección derivada de la fuente única** (el ledger), no dos copias editables.
- Regla: al añadir un agregado cacheado, enumera TODOS los caminos que mutan la fuente (insert, desvincular, anular) — todos deben recomputar. Ver [[postgres-guard-transition-no-persiste-en-recompute-chain]].
