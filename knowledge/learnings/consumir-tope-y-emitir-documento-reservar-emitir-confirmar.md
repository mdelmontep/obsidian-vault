---
title: consumir un tope Y emitir un documento fiscal → reservar-emitir-confirmar, no un RPC monolítico
date: 2026-07-18
source: claude-code-session facturaia
tags: [fiscal, supabase, postgres, transacciones, arquitectura, facturaia]
---

El motor de emisión de TuFacturaIA (`createDocument`) es TypeScript y NO es una única transacción: solo el sub-RPC SQL `create_factura_with_lineas` (mig 094) numera+cabecera+líneas+huella VeriFactu atómicamente; PDF/audit/FX/intracom son pasos TS posteriores best-effort. `anularFactura` tampoco es transaccional cross-table (idempotencia + orden + constraints).

Consecuencia: si un flujo debe CONSUMIR un tope/acumulador de forma atómica (ej. `obras.importe_facturado_acumulado`) Y emitir el documento, NO puedes meter la emisión en la transacción SQL del tope. Un RPC que llame directo a `create_factura_with_lineas` se salta composición de totales, reparto de descuento, FX, validaciones fiscales RD 1619/2012, PDF y audit → documentos rotos.

Patrón correcto (compensación, no 2PC): (1) RPC SQL atómico `reservar` (`SELECT ... FOR UPDATE` + valida tope + incrementa acumulado + fila estado='reservada') → cierra el race de doble-emisión; (2) emitir vía el motor TS; (3) RPC `confirmar` (vincula doc_id); (4) `revertir` en catch (idempotente); (5) cron reconcilia reservas huérfanas (>N min). Invariante de salud: acumulado == SUM(reservas 'emitida' con doc no anulado) — derivable y verificable.

**El reconciliador debe RECUPERAR HACIA DELANTE, no solo revertir** (hallazgo /fia-cierre): si `confirmar` falla tras un emit exitoso, la reserva queda 'reservada' pero el documento YA existe. Un cron que solo revierte reservas huérfanas >N min DESHARÍA una emisión legítima (descuadre del acumulador). Correcto: por cada reserva huérfana, buscar el documento emitido de esa entidad por su importe (base) sin vincular; si existe → `confirmar` (vincular); si no → `revertir`. Nunca auto-revertir una emisión real.

**Comparar el invariante con la MISMA magnitud**: el acumulador guarda base NETA (sin IVA). Compararlo contra Σ`total` (con IVA) da ~21% de desfase permanente → un banner "revisar" falso en toda entidad facturada. Sumar `base`, no `total` (el contratado también es neto).

Caso: facturación/certificación de obra (D4, issues 009/010), 2026-07-18. Ver [[verifactu-rpc-atomico-cierra-race-transacciones-rest-separadas]] (atomicidad del sub-RPC) y [[upsert-atomico-rpc-vs-check-then-act-evita-lost-update]].
