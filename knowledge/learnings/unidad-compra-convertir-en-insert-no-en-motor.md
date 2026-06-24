---
title: unidad de compra (cajas) — convertir en el RPC de inserción, no en el motor de stock
date: 2026-06-24
source: claude-code-session
tags: [facturaia, stock, arquitectura]
---

Modelo ERP "unidad de compra ≠ unidad de stock" (comprar en cajas, stock/coste por unidad): NO toques el motor probado (PMP/COGS/VeriFactu/sobreventa). Haz la conversión caja→unidad base **en el RPC que inserta la línea** (`aprobar_recibida_con_lineas`), server-side, leyendo el factor real del producto.

- La línea se guarda SIEMPRE en unidad base: `cantidad = cajas × factor`, `precio_unitario = precio_caja ÷ factor`.
- `subtotal` y la reconciliación Σlíneas-vs-base se calculan con los valores ORIGINALES (importe = cajas × precio_caja) → economía y VeriFactu idénticos.
- El motor de stock lee unidad base → entra el nº correcto de unidades al coste/ud correcto, sin tocarlo.
- Guarda `unidad_medida` + `cantidad_presentacion` solo para MOSTRAR fiel ("2 cajas"). Es capa de presentación.
- Corolario UI: cualquier badge que compare "precio de la línea vs PMP" debe usar el precio **ya convertido a /ud**, no el precio por caja (si no, marca "+650%" falso).

Caso: TuFacturaIA mig 384 (#471/#475). Relacionado: [[agregado-cacheado-sobre-ledger-recompute-trigger]].
