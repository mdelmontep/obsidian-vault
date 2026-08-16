---
title: una columna de precio que se puede rellenar sin que exista el cobro acaba anunciando humo
date: 2026-08-16
source: claude-code-session
tags: [facturaia, billing, stripe, pricing, modelo-de-datos]
---

`plan_features.addon_purchasable` + `addon_price_eur` se podían poner a mano sin que existiera un
`Price` vivo en Stripe. Resultado, **tres veces el mismo fallo**: `firma` con tarjeta y precio sin
checkout detrás (motivó ADR-013), «Conciliación bancaria +19 €/mes» que no es comprable en ningún
plan, y «multiempresa +30 €/mes» cuando el cobro real son **12 €/mes** por otra vía.

El patrón: **si el precio mostrado vive en un sitio distinto del que cobra, divergen**. No es
disciplina, es que el modelo lo permite. Y no lo caza ningún test: las dos columnas son válidas por
separado.

Arreglos, en este orden:
1. Derivar «comprable» de que exista cobro vivo (`estado='publicado' && precioVivo`), y el precio de
   la fila activa de precios. Así el botón sin cobro detrás es **irrepresentable**.
2. Una invariante que compare mostrado↔cobrado mientras convivan las dos fuentes, y que **muera con
   la columna** (dejarlo escrito en el issue del `DROP`, o el borrado tumba el typecheck).
3. Medir contra producción antes de retirar nada: aquí, `SELECT ... FROM plan_features WHERE
   addon_purchasable` en 30 segundos dijo qué se vendía de verdad y qué era ficción.

Vigilar también la documentación: el mismo precio falso estaba repetido en cuatro sitios (manual de
admin, doc de producto, manual de arquitectura y un upsell de la propia app).
