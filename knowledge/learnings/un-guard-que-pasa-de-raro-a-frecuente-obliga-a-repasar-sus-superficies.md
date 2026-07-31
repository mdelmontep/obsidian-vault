---
title: un guard que pasa de raro a frecuente obliga a repasar todas sus superficies
date: 2026-07-31
source: claude-code-session
tags: [guards, ux, metodo, regresion]
---
Al arreglar un guard que apenas se disparaba (colgaba de un flag calculado una vez: cubría
**1 de 14** casos) pasó a saltar siempre que toca: **6 de 24** documentos lo activan ahora.

El arreglo era correcto. El problema es el segundo orden: **el error que antes casi nadie
veía ahora lo ve todo el mundo**, y las superficies que lo reciben estaban escritas para un
caso raro. Cubrí dos pantallas y me dejé otras dos, que el gate de cierre encontró:

- una caía en el copy pensado para el proceso en lote ("hazlo de una en una para ver con
  cuál choca") **que era justo lo que el usuario estaba haciendo**;
- el swipe del móvil no tenía rama para ese resultado: no aprobaba y **no decía nada**, la
  fila reaparecía sin explicación.

Regla: al cambiar la frecuencia con la que se dispara un error, **grepea su código de error
y visita TODOS los sitios que lo reciben**, no solo el que motivó el cambio. Antes eran
callejones aceptables porque casi nunca se entraba en ellos; ahora son el camino normal.

Corolario que sí funcionó: hacer el mapa de resultados un `switch` exhaustivo sobre un tipo
propio. Una salida nueva sin rama pasa a romper el typecheck en vez de callarse, que era
exactamente el fallo. Caso real: FacturaIA `qa-030`.
