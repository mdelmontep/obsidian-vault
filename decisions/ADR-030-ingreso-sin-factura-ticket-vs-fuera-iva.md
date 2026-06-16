---
title: ADR-030 — Ingreso sin factura: ticket (simplificada) para ventas, "sin factura" solo para no sujetos
date: 2026-06-16
status: accepted
tags: [adr, facturaia, fiscal]
---

## Contexto

Autónomo en régimen general recibe cobros B2C sin emitir factura. El IVA **se devenga con la operación** (LIVA art. 75), no con la factura → una venta debe ir al 303 aunque no se facture. La función "registrar ingreso sin factura" (PR #270, mig 300, en prod 2026-06-16) lo deja **fuera de IVA**, lo que para una venta oculta IVA repercutido. El 303 se construye desde el **libro registro de facturas expedidas** (Holded igual: no mete IVA al 303 sin documento).

## Opciones consideradas

- **A** — Todo "ingreso sin factura" fuera de IVA → simple, pero oculta el IVA de las ventas (ilegal).
- **B** — Computar la cuota al 303 desde el importe sin emitir documento → declara el IVA pero genera repercutido sin soporte en el libro registro (irregular en inspección).
- **C** — Factura **simplificada** (ticket, RD 1619/2012 art. 7, sin DNI ≤400€) para ventas; "ingreso sin factura" reservado a **no sujetos** (subvención/interés/indemnización…) con motivo obligatorio, fuera del 303.

## Decisión

**C**. La venta se factura con ticket (IVA al 303 vía libro + Verifactu F2); el path "sin factura" solo registra ingresos genuinamente no sujetos. Plan en `issues/prd-factura-simplificada.md` (issues 094-099).

## Consecuencias

Cerramos la opción de "ingreso con IVA sin documento". Editar el NIF de una factura emitida queda prohibido (inalterable; Verifactu encadena hash) → solo factura rectificativa. Diferido: convertir ticket→factura completa con NIF, factura-e B2B 2026. Relación: [[ADR-029-conciliacion-casos-asientos-no-ledger]].
