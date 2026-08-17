---
title: al revisar trabajo ajeno, muta la propiedad que la pr declara como su aportación
date: 2026-08-17
source: claude-code-session
tags: [testing, mutacion, revision, agentes]
---

Lo que el autor **argumenta** en el cuerpo de la PR es justo lo que nadie **asevera**: escribe el
candado para el caso que tenía en la cabeza y da por probado el razonamiento que justifica el diseño.

Medido en agh-iberica (17-ago, 6 tracks): de ~11 mutaciones de revisión distintas de las del autor,
**dos SIN VÍCTIMA y las dos huecos reales**, ambas sobre la frase-aportación de su PR — «funciona
aunque venga con los códigos ANSI» (borrar el `replace`: 97→97 passed) y «el presupuesto es del
barrido, no de cada proyecto» (quitar el descuento: 211→211).

🔴 **Y el dato que cambia cómo se lee un barrido:** `mutate:diff` había dado **`0 SIN VÍCTIMA`** en
esa rama — 14 con víctima y **14 «sin medir» por crash** — y aun así la mutación quirúrgica
sobrevivió. Revertir el hunk entero no compila y cae en «sin medir»; borrar **solo la llamada**
dejando la variable sí compila y mide. **`0 SIN VÍCTIMA` no significa cubierto mientras «sin medir»
no sea 0**: ahí se esconde lo que el barrido no pudo preguntar.

**Cómo aplicarlo:** subraya cada propiedad que la PR declara como suya · muta cada una con la mínima
edición que **compile** · mira el recuento de «sin medir» antes de creerte un `0 SIN VÍCTIMA` · y al
devolver el trabajo, pide buscar **la misma forma** en el resto del diff (ahí salieron 3 casos más, y
uno de los arreglos tampoco bastó a la primera).

Ver [[el-hueco-esta-en-el-cableado-no-en-la-funcion-pura]] ·
[[un-arnes-de-mutacion-sobre-vitest-no-ve-los-candados-de-tipos]] ·
[[arnes-con-asserts-de-eco-y-falso-verde-no-detecta-nada]]
