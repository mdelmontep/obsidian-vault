---
title: ADR-019 — precio "con IVA incluido" (Holded-style) en form FacturaIA: storage canónico vs columna precio_modo vs doble columna
date: 2026-05-24
status: accepted
tags: [adr, facturaia, fiscal, ux-vs-storage]
---

## Contexto
Form `/generar` de factura: feedback usuario "el precio que escribo debe ser ya con IVA, estilo Holded". Implica decisión arquitectónica con impacto en Verifactu hash, AEAT 303, reportadores SQL, calculador IRPF. La factura legal SIEMPRE muestra desglose base+%+cuota+total (RD 1619/2012 art 6.1.f-g + LIVA art 88.Uno), así que la cuestión es solo cómo capturar el input.

## Opciones consideradas
- **A** — Storage canónico = base imponible neta (sin migración). Toggle UX por documento (`sessionStorage[doc_id]`) + default org (`default_precio_iva_incluido`). Conversión client-side al guardar. PROS: cero migración data, retrocompatibilidad, hash Verifactu estable. CONS: si user cambia toggle a mitad de captura, recálculo en UI (manejado con modal confirm "preservar total" | "mantener números").
- **B** — Columna `lineas_factura.precio_modo TEXT IN ('bruto','neto')`. Cada línea sabe cómo se introdujo. PROS: auditable, sin recálculo en UI. CONS: ramifica cálculo IVA en 4 RPCs SQL (mig 094/088/036/038) + voice/totals.ts + calculador 303 + Verifactu canonical. Doble fuente de verdad.
- **C** — Doble columna `precio_base_x100` + `precio_total_x100` siempre poblados. PROS: sin ambigüedad de cálculo. CONS: redundancia con riesgo divergencia tras edits parciales; doble peso datos sin valor añadido.

## Decisión
**A**, porque Verifactu sella base imponible y AEAT 303 lee base; cualquier "fuente alternativa" introduce drift por redondeo en CADA lectura → hash inestable, reportadores divergentes. El coste de A (modal confirm al alternar toggle con líneas pobladas) es 1 UI, no N puntos de mantenimiento.

## Consecuencias
- Mig 161 solo añade flag UX `organizations.default_precio_iva_incluido` (no afecta cálculo). Sin migración de data.
- Toggle implementado como `useState` + `sessionStorage` por documento, NO por línea en BD.
- Helper `calcularLinea(l, inclusive)` aplica `precioToBase` SOLO en pipeline serialización. Tests 27/27 cubren equivalencia matemática inclusive ↔ neto.
- PDF (4 templates) renderiza desglose siempre — el toggle es invisible al cliente final.
- Ver [[toggle-ux-only-no-contamina-storage-canonico-fiscal]] para patrón generalizable.