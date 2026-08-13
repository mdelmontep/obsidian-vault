---
title: una media ponderada acumulada no se corrige repitiendo la operación buena
date: 2026-08-01
source: claude-code-session
tags: [contabilidad, postgres, stock, datos]
---
Un valor que se calcula **incrementalmente sobre sí mismo** (coste medio ponderado, rating medio,
saldo con interés) no se arregla borrando el documento malo ni volviendo a aplicar el bueno: el
error ya está dentro del acumulado y la operación nueva pondera **encima** del valor sucio.

Caso TuFacturaIA: `catalogo_servicios.coste_medio` (PMP) subía con cada compra
`nuevo = (stock·pmp + qty·coste)/(stock+qty)`. Borrar la compra errónea lo dejaba torcido para
siempre («OSTRA Nº3»: 36,6250 € con 3 de 5 unidades entradas a 37 € por el albarán a anular).

- Fix: **rehacer el valor desde el ledger** con la MISMA aritmética que lo escribe (`recompute_pmp`
  recorre los movimientos en orden; solo las compras mueven la media; reset si el stock previo ≤ 0).
- Se decidió pisar un valor tecleado a mano, mismo criterio que ya se aplicaba a `stock_actual`: el
  libro manda. Para que no sea invisible, devolver **antes/después por entidad** al `audit_log` y una
  cifra al aviso de la UI. Ver [[ADR-045-el-coste-medio-se-rehace-desde-el-ledger-al-revertir-una-compra]].
- Si al recalcular no queda ninguna operación con la que calcularlo, **conservar el valor anterior**;
  vaciarlo rompe lo que lea después (aquí, el COGS de las ventas).

**Secuela 13-ago**: `recompute_pmp` seguía sin filtrar por `lote_id`, mientras `recompute_stock`/
`recompute_lote` (mig 312) ya excluían movimientos sin partida en productos con lotes desde meses
antes. Dos funciones sobre el MISMO ledger con criterio distinto: la cantidad ya ignoraba una compra
huérfana, el coste seguía viéndola. Misma «OSTRA Nº3» — el "5 duplicado" del hub resultó ser DOS
compras huérfanas de la misma mañana, no una. Regla: cuando un ledger alimenta varios agregados
derivados (cantidad Y coste), un cambio de criterio de filtrado (aquí, lote-aware) tiene que tocar
TODOS los que derivan de él, no solo el que motivó el fix original.
