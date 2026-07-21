---
title: css grid con cabecera y filas en grids separados — columnas auto/fr no sincronizan anchos
date: 2026-07-21
source: claude-code-session
tags: [css, grid, frontend]
---
Una fila de cabecera (`.tableHead`) y N filas de datos (`.row` por elemento, cada una su propio `display:grid`) con el MISMO `grid-template-columns` no quedan alineadas si alguna columna usa `auto`/`fr`: cada grid container calcula el ancho de sus columnas `auto` por SU PROPIO contenido. La cabecera ("PP" suelto) y la fila (checkbox + "PP") difieren en ancho → todo lo de la derecha (siguiente columna, importe) queda descuadrado, aunque el CSS "se vea" idéntico.

Fix: columnas no-`fr` con `px` fijo en AMBOS selectores (cabecera y fila), nunca `auto`. Solo la columna de contenido variable (descripción larga) puede ser `1fr`/`fr` sin romper alineación, porque `fr` reparte espacio sobrante sin depender de su propio contenido — pero si OTRA columna `auto` en el mismo template varía de ancho entre grids, el espacio sobrante también varía y el `fr` se desalinea en cascada.

Caso real: TuFacturaIA, cabecera "Concepto/Cantidad/PP/CMO/Importe" sobre filas de partida de presupuesto — commit `ad6e6e3c`.
