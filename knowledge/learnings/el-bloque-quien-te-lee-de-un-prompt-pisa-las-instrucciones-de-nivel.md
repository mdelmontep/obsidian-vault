---
title: el bloque «quién te lee» de un prompt pisa cualquier instrucción de nivel
date: 2026-08-11
source: claude-code-session
tags: [prompting, claude, contenido]
---
Un generador de contenido escribía siempre por encima del nivel pedido. La causa no estaba en el
bloque de nivel —que decía "desde cero, define cada término"— sino en el de audiencia:

> «founder y desarrollador **sénior**. Sabe de sobra qué es una tabla, un contenedor, una API. Eso
> NUNCA se explica: sería insultante.»

Con eso puesto daba igual lo que dijera el nivel. La caracterización del lector gana a las reglas de
estilo, porque el modelo la usa para decidir qué dar por sabido.

Dos correcciones, y las dos hicieron falta:
1. **Describir al lector con precisión**, incluido lo que NO sabe. "Construye cosas en producción
   pero no viene de informática académica, así que el vocabulario del campo no lo tiene aunque a
   veces ya aplique el concepto sin saber que se llamaba así."
2. **Una regla de orden, no de cantidad**: ninguna palabra técnica aparece antes de que el lector
   entienda la idea que nombra. Escena concreta → qué se rompe → cómo se arregla → *entonces* el
   nombre. Medible: dónde aparece el término, en % del texto.

Al depurar un prompt que no obedece, mirar primero la descripción del destinatario.
