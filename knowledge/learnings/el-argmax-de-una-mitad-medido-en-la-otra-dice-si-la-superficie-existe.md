---
title: el argmax de una mitad, medido en la otra, dice si la superficie de parámetros existe
date: 2026-07-31
source: claude-code-session
tags: [metodo, tuning, estadistica, verificacion]
---

Con N configuraciones **siempre** hay una mejor: eso es aritmética, no hallazgo. La prueba
barata de si el "punto óptimo" es real: elígelo mirando SOLO la mitad A y mira qué hace en
la mitad B, que no participó en elegirlo.

Caso (cryptobruj-bot, 480 configuraciones): el argmax de A daba **−0.282R en B —
percentil 0.01**, casi la peor de las 480. No es que la ventaja se encoja: se da la vuelta.

Y el segundo paso, que es el que de verdad informa: **descompón la correlación de rangos
fijando un eje**. La correlación global era +0.46 y parecía superficie sólida; fijando un
solo parámetro caía a +0.15/−0.29. Toda la estructura era **un eje**; los otros cuatro eran
ruido con relieve, y "optimizarlos" era memorizar el pasado.

Aplicable a cualquier barrido: hiperparámetros, umbrales de alerta, pesos de scoring.
Reportar el percentil del ganador en la mitad de comprobación, no su valor en la de
elección. Ver [[reservar-datos-ciegos-y-preregistrar-parametros-antes-de-buscar]].
