---
title: ADR-040 — BtchBookg a true por defecto en las remesas SEPA
date: 2026-07-25
status: aceptada
tags: [adr, facturaia, sepa, conciliacion]
---

## Contexto

`BtchBookg` del `PmtInf` dice al banco del acreedor si apunta la remesa como un movimiento agregado (`true`) o uno por adeudo (`false`). Estaba fijo en `false`.

La auto-conciliación (`findUniqueMovimiento`) busca **un** movimiento cuyo importe sea exactamente `ctrl_sum`. Con el apunte desglosado ese movimiento no existe, y además N adeudos del mismo importe son ambiguos entre sí. Le pedíamos al banco lo contrario de lo que el propio módulo necesita.

## Alternativas

1. **Dejarlo en `false`.** Cero riesgo, pero la auto-conciliación sigue sin casar nunca y el módulo promete algo que no cumple.
2. **Cambiarlo a `true` fijo.** Arregla la conciliación, pero cambia el extracto de todas las orgs que ya domicilian sin darles salida.
3. **Exponerlo como ajuste, default `true`.** Elegida.

## Decisión

Opción 3. El default arregla el caso mayoritario y quien cuadre a mano contra el extracto desglosado puede desactivarlo.

## Consecuencias

- **Cambia el extracto bancario de las orgs que ya usan el módulo** desde la siguiente remesa: un apunte agregado en vez de uno por recibo.
- Bastantes entidades españolas ignoran la etiqueta y aplican lo pactado en el contrato de adeudos. Es "pedirlo bien", no garantizarlo.
- Si un banco netea las devoluciones antes de apuntar el total, el agregado deja de coincidir con `ctrl_sum` y la conciliación falla igual. No observado todavía.
- Fichero verificado con una remesa real el 2026-07-25 (`BtchBookg` a `true` en el XML). Queda confirmar en el extracto bancario, tras la primera remesa post-deploy, que el banco lo respeta.

Ver [[btchbookg-false-contradice-la-autoconciliacion-lump-sum]] · [[facturaia-modulo-sepa-config]].
