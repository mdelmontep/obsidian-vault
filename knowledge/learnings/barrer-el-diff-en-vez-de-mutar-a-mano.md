---
title: mutar a mano solo cubre tu hipótesis — barre el diff
date: 2026-08-07
source: claude-code-session
tags: [testing, mutacion, metodo, verificacion, gate]
---
Mutar a mano cubre **aquello sobre lo que ya tienes una hipótesis**, así que por definición no llega a
lo que no se te ocurrió. AGH 7-ago: en una tanda, mutaciones declaradas 12 · 9 · 7 · **0**. El dato que
manda es la de **9** — se coló un defecto igual, porque las nueve caían sobre los ejes que la PR había
diseñado y **ninguna tocó un sitio de llamada que el diff no editaba**.

El **diff sí es la lista objetiva** de lo que la rama afirma haber añadido. Revertir cada cambio y
exigir víctima no depende de que se te ocurra el ataque. Hacen falta **dos granularidades**: un guard
de una línea dentro del hunk que añade la función entera queda enterrado (revertir el hunk mata 20
tests → «víctima»), así que tras la pasada de hunks va otra **línea a línea dentro de los que sí
tuvieron víctima**.

Al leer el resultado, dos trampas que dan **verdes falsos**: un rojo por **crash** (borrar un `const`
usado más abajo) no es un candado, y **ficheros en rojo con CERO tests en rojo** significa que no se
ejecutó una aserción. Los dos son «no medido», nunca «vigilado». Y un hueco puede ser **mutante
equivalente**: se declara por escrito con la prueba de por qué ningún input los distingue.

Relacionado: [[verificar-que-un-test-tiene-dientes-con-una-mutacion]] ·
[[arnes-con-asserts-de-eco-y-falso-verde-no-detecta-nada]]
