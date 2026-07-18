---
title: consumir un tope Y emitir un documento fiscal → reservar-emitir-confirmar, no un RPC monolítico
date: 2026-07-18
source: claude-code-session facturaia
tags: [fiscal, supabase, postgres, transacciones, arquitectura, facturaia]
---

El motor de emisión de TuFacturaIA (`createDocument`) es TypeScript y NO es una única transacción: solo el sub-RPC SQL `create_factura_with_lineas` (mig 094) numera+cabecera+líneas+huella VeriFactu atómicamente; PDF/audit/FX/intracom son pasos TS posteriores best-effort. `anularFactura` tampoco es transaccional cross-table (idempotencia + orden + constraints).

Consecuencia: si un flujo debe CONSUMIR un tope/acumulador de forma atómica (ej. `obras.importe_facturado_acumulado`) Y emitir el documento, NO puedes meter la emisión en la transacción SQL del tope. Un RPC que llame directo a `create_factura_with_lineas` se salta composición de totales, reparto de descuento, FX, validaciones fiscales RD 1619/2012, PDF y audit → documentos rotos.

Patrón correcto (compensación, no 2PC): (1) RPC SQL atómico `reservar` (`SELECT ... FOR UPDATE` + valida tope + incrementa acumulado + fila estado='reservada') → cierra el race de doble-emisión; (2) emitir vía el motor TS; (3) RPC `confirmar` (vincula doc_id); (4) `revertir` en catch (idempotente); (5) cron reconcilia reservas huérfanas (>N min). Invariante de salud: acumulado == SUM(reservas 'emitida' con doc no anulado) — derivable y verificable.

Caso: facturación/certificación de obra (D4, issues 009/010), 2026-07-18. Ver [[verifactu-rpc-atomico-cierra-race-transacciones-rest-separadas]] (atomicidad del sub-RPC) y [[upsert-atomico-rpc-vs-check-then-act-evita-lost-update]].
