---
title: ADR-005 — Código exención IVA per-línea (E1-E6) en lineas_factura
date: 2026-05-18
status: accepted
tags: [adr, facturaia, fiscal, verifactu]
---

## Contexto
RD 1619/2012 art 6.1.j + Verifactu L10 (E1-E6) exigen indicar causa de exención IVA. Facturas pueden tener líneas mixtas (21% + exenta art 20 + exenta art 25 a la vez).

## Opciones consideradas
- **A — `facturas.norma_exencion TEXT`** — texto libre per-factura. AEAT no acepta texto, solo códigos.
- **B — `facturas.norma_exencion_codigo` enum** — un solo código per-factura. Falla en facturas mixtas.
- **C — `lineas_factura.exencion_codigo` enum E1-E6** — cubre 100% casos XSD.
- **D — JSONB array** — duplica info de líneas.

## Decisión
**C**, porque XSD acepta múltiples `DetalleDesglose` con códigos distintos por factura.

## Consecuencias
Cualquier flow que cree líneas (createDocument, voice/generate, RPC convertir, presupuestos JSONB) debe propagar `exencion_codigo`. UI muestra selector reactivo si `iva_pct=0`. CHECK BD blinda consistencia. Verifactu agrupa por `(iva_pct, exencion_codigo)`.

Ver [[verifactu-xml-desglose-obligatorio-xsd-rechaza-sin-el]]
