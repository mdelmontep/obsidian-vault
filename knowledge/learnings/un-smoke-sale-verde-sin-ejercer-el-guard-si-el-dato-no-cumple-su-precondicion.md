---
title: un smoke sale verde sin ejercer el guard si el dato no cumple su precondición
date: 2026-08-26
source: facturaia — smoke de albaranes en prod (#2209, mig 754)
tags: [testing, smoke, guards, facturaia]
---

El guard del doble conteo de stock vive en `aplicar_movimientos_stock`: si la línea de la
factura ya la asentó un albarán, no la vuelve a mover. En el smoke sobre producción crucé el
albarán con la factura, la aprobé, y el stock **no** se duplicó. Verde.

Pero la línea de esa factura no tenía `catalogo_id`, y sin él la función ni siquiera llega a
preguntar por el albarán: no mueve stock **por otra razón**. El guard no se ejerció. El
resultado observable (stock correcto) era idéntico con el guard puesto y con el guard fuera.

Antes de dar por probado un guard, comprobar que el dato del smoke cumple la precondición que
lo activa — la columna que lo dispara, el estado que lo enciende. Si no la cumple, el verde
mide otro camino. Y la comprobación barata es la de siempre: quitar el guard y ver si el smoke
se pone rojo. Mismo principio que [[guard-de-migracion-que-recalcula-la-formula-no-verifica-nada]]
y que el arnés que se mide a sí mismo.
