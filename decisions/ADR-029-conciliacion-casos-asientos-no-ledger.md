---
title: ADR-029 — Casos contables de conciliación (préstamos/suplidos/compensación) sin ledger
date: 2026-06-13
status: accepted
tags: [adr, facturaia, conciliacion]
---

## Contexto
Tres casos de Holded (préstamos, suplidos, compensación compra↔venta del mismo
contacto) asumen contabilidad de doble partida (asientos multilínea, cuentas PGC
520/626/555/768/668). TuFacturaIA es facturación + conciliación bancaria, sin
libro diario ni asientos. Issue `058` del PRD `prd-conciliacion-holded-avanzado`.

## Opciones consideradas
- **A — Construir módulo de ledger** — fidelidad contable total; meses de trabajo, convierte el producto en un ERP y replantea posicionamiento.
- **B — Aproximar por categorización** — préstamo→2 categorías (capital/intereses), suplido→categoría+nota, compensación→ambos movs categorizados+nota; cubre ~80% del valor (visibilidad) sin saldos contables automáticos.
- **C — Fuera de alcance** — solo export de movimientos categorizados; el asiento lo hace la asesoría.

## Decisión
**Ninguna se implementa ahora.** Se descarta el ledger (A) por posicionamiento.
La aproximación por categorización (B) se adopta como **dirección documentada
para ampliar la oferta en el futuro**, no como trabajo de este sprint. Hoy estos
casos se cubren de facto con las primitivas existentes (categorías + notas +
"resto" de 050/053) y, si hace falta, export a la asesoría (C).

## Consecuencias
- No se construye libro diario / cuentas PGC. Si el mercado lo exige, se reabre como decisión nueva (gran esfuerzo, cambio de posicionamiento).
- Cuando se priorice, abrir issues hijos por caso (préstamo, suplido, compensación) implementando B sobre las primitivas actuales — sin ledger.
- Issue `058` se cierra como DECIDIDO (no implementable hasta priorizar B). 055 (anticipos, entidad nueva) y 057 (divisa, resto categorizado) sí se implementan en este ciclo.
