---
title: una diferencia de duración entre corridas separadas mide la hora, no el código
date: 2026-09-20
source: agh-iberica
tags: [metodo, medicion, gate, testing]
---

Gate rojo **tres veces en tres ficheros distintos**, siempre por timeout de hook y nunca por
aserción, ninguno tocado por el diff. Con esa firma de rojo ajeno ya completa, miré las duraciones
del día —otras ramas a 354 s y 347 s, la mía a 705 s y 492 s— y concluí que **el lento era mi diff**.
Falso: iban separadas por media hora, un arnés de UI y un push ajeno. Entrelazado —`main` en el MISMO
worktree justo antes, mi rama justo después— salió `main` 305 s y la rama **217 s**.

Una diferencia de duración solo habla del código si las dos corridas son **contiguas y en el mismo
worktree**: `git checkout --detach origin/main` → correr → volver a la rama → correr. Si no puedes
entrelazarlas, no tienes la medición: tienes la hora.

Y el sesgo: tres rojos encima hacen comodísima la hipótesis «es mío», cuando tres ficheros distintos
son justo la prueba de lo contrario. Ver
[[tests-que-caen-por-contencion-de-cpu-verificalos-aislados-antes-de-diagnosticar]] y
[[medir-un-cambio-contra-un-llm-entrelazado-no-en-bloques]].
