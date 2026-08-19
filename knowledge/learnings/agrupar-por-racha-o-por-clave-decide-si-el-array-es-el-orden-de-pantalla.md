---
title: agrupar por racha o por clave decide si el array de datos es el orden de pantalla
date: 2026-08-19
source: claude-code-session facturaia
tags: [react, listados, ui, tests]
---

Dos maneras de pintar cabeceras de grupo en una lista, indistinguibles al mirarla:

- **por racha**: se abre grupo nuevo cuando el valor cambia respecto al item ANTERIOR. Aplanar los
  grupos devuelve el array de entrada tal cual → el array **es** el orden de pantalla.
- **por clave**: el grupo se abre en la PRIMERA aparición y los siguientes se acumulan ahí. Eso
  **reordena**: un valor que reaparece más abajo salta hacia arriba.

Cualquier cosa que razone sobre "de esta fila a esta otra" (selección por tramo con Mayús, arrastrar,
`indexOf`, navegación con flechas) se rompe en silencio con la segunda: el tramo se salta las filas
del grupo intercalado. Con datos ordenados por la clave las dos formas coinciden, así que **un test
con listas planas u ordenadas no lo detecta** — el caso que discrimina es el valor que reaparece.

Casos reales (TuFacturaIA): facturas y presupuestos agrupan por clave y hubo que construir el orden
visual aparte; la bandeja de entrada agrupa por racha y ahí el array vale. La diferencia estaba en dos
bucles de diez líneas y en ninguna parte escrita. Ver
[[verificar-que-un-test-tiene-dientes-con-una-mutacion]].
