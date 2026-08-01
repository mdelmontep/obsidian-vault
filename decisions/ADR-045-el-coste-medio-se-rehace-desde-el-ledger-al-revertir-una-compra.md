---
title: ADR-045 — al revertir una compra, el coste medio se rehace desde el ledger aunque pise un valor tecleado a mano
date: 2026-08-01
status: accepted
tags: [adr, facturaia, stock, contabilidad]
---

## Contexto
Borrar una recibida ya revierte su entrada de inventario (mig 620). `catalogo_servicios.coste_medio`
(PMP) es un acumulado que sube con cada compra y **no se deshace solo**: reaprobar el documento
corregido pondera encima del valor sucio, así que el error no se va nunca. Y es un campo que el
usuario puede editar a mano en `/settings?tab=catalogo`.

## Opciones consideradas
- **A — No tocarlo** (lo que hacía la 1ª versión): respeta el valor humano, pero deja un precio falso
  que ni reaprobando se arregla. En el ticket nº130, 3 de 5 unidades a 37 € venían del albarán anulado.
- **B — Recalcular desde el ledger**: precio correcto y determinista, pero pisa un valor tecleado.
- **C — Invertir solo la aportación de esa compra**: conserva el edit humano, pero es aritmética
  frágil (dos reversos seguidos, o un edit intermedio, dan un número que no describe nada).

## Decisión
**B**. El libro manda, que es el criterio que la mig 567 ya aplicaba a `stock_actual` (también
ajustable a mano y también reproyectado). Se mitiga la pérdida haciéndola visible: `pmp_detalle`
(producto, antes, después) al `audit_log` y la cifra en el aviso de borrado. Si al producto no le
queda ninguna compra, se conserva el valor previo en vez de vaciarlo (un `coste_medio` NULL rompe el
COGS de las ventas).

## Consecuencias
Un coste medio afinado a mano se pierde si esa reversión toca el producto, y el usuario lo lee en el
aviso. Cerramos la opción de tratar `coste_medio` como dato de entrada del usuario: pasa a ser una
proyección del ledger, como el stock. Ver
[[una-media-ponderada-acumulada-no-se-corrige-repitiendo-la-operacion-buena]].
