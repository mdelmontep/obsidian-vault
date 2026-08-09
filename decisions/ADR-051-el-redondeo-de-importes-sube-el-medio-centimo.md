---
title: ADR-051 — el redondeo de importes sube el medio céntimo (variante con Number.EPSILON)
date: 2026-08-09
status: accepted
tags: [adr, facturaia, dinero, fiscal]
---

## Contexto

TuFacturaIA tenía **55 copias** de la misma operación de redondeo repartidas por `src/`, en dos variantes que no dan lo mismo: `1.005` → **1.01** con `Number.EPSILON`, **1.00** sin él. La única nota que documentaba la divergencia estaba enterrada en un comentario de una tool del copiloto y decía «divergencia DELIBERADA, no unificar». El resultado dependía de qué copia tocara ese camino del código.

## Opciones consideradas

- **A — con `Number.EPSILON`**: el `x,xx5` sube de forma estable. Es lo que ya hacían ~42 de las 55 copias, incluida `create-document.ts`, que emite las facturas reales.
- **B — sin EPSILON** (`Math.round(n*100)/100`): más simple de leer, pero `1.005` baja a 1.00 porque en binario ese número es 1.00499…, así que redondea al revés de lo que escribió el usuario.
- **C — céntimos con `BigInt`** en todo el producto: exacto, pero obliga a reescribir toda la capa de importes que hoy viven como `number`.

## Decisión

**A**, decidida por el dueño del producto. El canónico vive en `src/lib/dinero/redondeo.ts` (`roundCent`, `roundN`) y las 55 copias pasan a importarlo. `src/lib/fiscal/**` queda fuera: ya usa **C** (céntimos con `BigInt`) y ahí no hay nada que redondear.

## Consecuencias

Una sola aritmética del dinero en el producto, y la decisión queda fijada por tests que comparan explícitamente contra lo que daba la variante retirada. Se conserva la precisión distinta de 4 decimales (precios unitarios de obra) y 3 (stock) vía `roundN(n, dec)`: unificar no puede aplastarlas a 2.

Medido antes de tocar nada: 3.019 tests de importes en verde; después, los mismos 3.019. **Ningún importe cubierto por la suite se mueve** — la unificación no cambia resultados, solo elimina el azar. PR #1572. Ver [[el-redondeo-del-medio-centimo-decide-el-iva]].
