---
title: una columna que aloja un control necesita un ancho por tipo de puntero
date: 2026-08-08
source: claude-code-session
tags: [css, design-system, accesibilidad, frontend, testing]
---

Corolario de [[el-tap-target-del-boton-compartido-es-el-suelo-de-la-altura-de-fila]]:
si separas el botón por puntero (`min-width: 44px` táctil / `0` con ratón), el
botón deja de tener UN ancho — y la columna que lo contiene tampoco puede
declarar uno. Con la pista dimensionada al caso ratón, en tableta dos botones de
44 suman 90 dentro de 68 y, con `justify-content: flex-end`, lo que sobra se
desborda por la IZQUIERDA y pisa la columna de al lado.

No se ve en revisión: el desarrollo es con ratón, y el contexto roto es el otro.

- Ancho de columna a variable, con el TÁCTIL de valor por defecto y el
  `@media (pointer: fine)` bajándolo — espejo del propio botón. Si el navegador
  no informa del puntero, peca de columna ancha, no de columna pisada.
- El ancho total de la rejilla, con `calc()` sobre esas variables. Un literal
  sincronizado a mano entre dos contextos se desincroniza en uno.
- El test debe LEER el tamaño del botón de su fichero, no fijar 44/32 a pelo: con
  literales, subir el botón a 48 deja el test verde y devuelve el bug.
- Ojo al control que solo existe en cierto estado (un «guardar» que aparece al
  tocar la fila): no está en el DOM en reposo, así que ni captura ni smoke normal
  lo ven. Hay que teclear de verdad para medirlo.

Ver [[facturaia]].
