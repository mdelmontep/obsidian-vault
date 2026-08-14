---
title: mide cuántos pueden fallar antes de elegir entre N candados y un tripwire
date: 2026-08-14
source: claude-code-session
tags: [tests, invariantes, diseno, medicion]
---

Un helper de test tenía un punto ciego estructural (solo veía la regla base del CSS, nunca las
`@media`). El arreglo obvio: aserción responsive en todos los candados. **La cifra lo descartó.**

Instrumentado el helper para registrar cada par `(selector, propiedad)` en la corrida real —así entran
los de bucles con template literals, que un grep no ve— y cruzado contra el CSS:

**141 pares aseverados. Solo 4 tenían variante dentro de una at-rule (2,8 %).**

Cubrir los 141 habría dejado **137 clases incapaces de fallar**, cuyo silencio se lee como cobertura.
Así que la clase se cierra **en el instrumento**: el helper **lanza** si la propiedad que le pides está
redeclarada en una at-rule, y los 4 vivos se cubren uno a uno con la invariante que cada uno tenga.

👉 **Lo que hay que impedir no es el caso 4, es el caso 142.**

Y la premisa se quedó corta por un lado inesperado: de 16 bloques `@media`, **13 eran feature queries**
(`hover`, `pointer`, `prefers-reduced-motion`), no breakpoints — un arreglo acotado a «responsive» se
habría dejado uno fuera. Ver [[un-guard-sin-medir-cementa-una-premisa-falsa]].
