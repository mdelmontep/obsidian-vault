---
title: si la variante se elige por el contenido, el candado por línea es ciego a las demás
date: 2026-08-07
source: claude-code-session
tags: [testing, qa, metodo]
---
Para que un texto generado no suene a plantilla se elige una variante de un pool. La elección tiene
que ser **determinista** —`Math.random()` hace irreproducible el test y no comparable una corrida de
evals— así que se deriva del contenido: mismo dato, misma frase; datos distintos, frases distintas.

El efecto secundario no se ve: **un caso de prueba ejercita SIEMPRE la misma variante**. Un test que
asevera sobre la línea renderizada es estructuralmente ciego a las otras N-1, que pueden perder el
dato que incrustan con toda la suite en verde. Lo delató una mutación: vaciar una variante del pool
no tumbaba nada.

**Fix: la invariante es del POOL, no de la línea.** Exportar el pool y recorrerlo entero comprobando
la propiedad («toda variante incrusta la carga»). Y al aseverar sobre la línea, no basta la
pertenencia al molde: hay que exigir que **entre prefijo y sufijo quede algo**, o el molde encaja
igual con el dato perdido.

Para partir un molde por su hueco hace falta un testigo — **nunca un NUL**: pasa lint, typecheck y
tests, y deja el fichero invisible a `grep`. Un token visible (`__CARGA__`) hace lo mismo y se busca.
