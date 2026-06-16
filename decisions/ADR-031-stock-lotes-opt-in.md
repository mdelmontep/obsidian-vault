---
title: ADR-031 — Stock por partidas/lotes: opt-in híbrido por producto
date: 2026-06-16
status: accepted
tags: [adr, TuFacturaIA, stock]
---

## Contexto
Cliente (pescadería) compra el mismo producto en partidas con coste/calidad/caducidad
distintos y necesita elegir de qué partida sale cada línea al facturar (trazabilidad
alimentaria + COGS real por lote). El stock era un único agregado por producto.

## Opciones consideradas
- **A** — Calidades = productos distintos del catálogo: cero esquema, pero no da trazabilidad de lote ni coste por entrada.
- **B** — Lotes obligatorios para todo producto con stock: trazabilidad total, pero impone la complejidad a todos los clientes del SaaS.
- **C** — Lotes opt-in por producto (`gestiona_lotes`): solo los que lo activan usan partidas; el resto sigue agregado.

## Decisión
**C**, porque la mayoría de clientes no necesita lotes y no deben pagar su complejidad.
Motor de lotes AISLADO (`aplicar_movimientos_lotes`); el motor agregado solo gana un
filtro `gestiona_lotes=false` y delega → diff mínimo en la ruta fiscal probada.

## Consecuencias
Invariante `stock_actual = Σ stock_lotes.cantidad_actual` para productos con lotes;
activar captura el stock agregado como partida `INICIAL`. Compra auto-crea partida;
venta descuenta la elegida y bloquea sobreventa. `lote_id` no entra en importes/huella
(VeriFactu intacto). mig 308 · PR #296. Ver [[nulls-not-distinct-idempotencia-con-discriminador-opcional]].
