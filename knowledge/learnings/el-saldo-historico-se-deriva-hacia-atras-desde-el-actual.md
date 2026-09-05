---
title: el saldo de una fecha se deriva hacia atrás desde el actual, no sumando el ledger
date: 2026-09-05
source: facturaia — ticket de soporte 171 (Pescados Chivite)
tags: [stock, ledger, medicion, facturaia]
---

Para saber qué stock había el día D hay dos caminos, y **solo uno es válido cuando
el ledger no reconcilia**: `saldo(D) = stock_actual − Σ movimientos posteriores a D`.
Sumar el ledger de cabo a rabo asume que el ledger ES la verdad; el saldo actual
suele serlo más, porque es lo que la app enseña y lo que el cliente ve.

Caso real: en Chivite la suma del ledger daba N1=48 y N2=92; la derivación hacia
atrás daba 21 y 60, que era lo correcto. La desviación (−27, −26, −3…) venía de una
migración vieja que dejó conviviendo compras sin partida con sus `apertura`
reconstruidas. Se detecta en un minuto: mide `stock_actual − Σ(ledger entero)` por
producto; si no sale 0, el ledger no reconcilia y la suma miente.

Corolario: la función de recálculo global (`recompute_stock`) **no repara, falsea**.

Y antes de comparar contra un recuento del cliente, comprueba que comparas la misma
población: aquí «N2» eran **tres fichas de catálogo**, y restar una contra las tres
inventó un hueco de 42 unidades que no existía. Ver [[un-conteo-con-grep-falla-en-silencio]].
