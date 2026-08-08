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

**Solo aplica si la columna tiene ancho DECLARADO.** Si la pista es `auto`, la
fila es flex o es un `<td>` de tabla real, se dimensiona sola y copiar aquí el
desdoble por puntero son dos números que mantener a mano sin motivo (medido el
8-ago en pedido y objetivos: ninguna lo necesitaba). Lo que sí conviene es
atornillar esa premisa en el test — que la pista siga terminando en `auto` —
porque cambiarla por un ancho fijo reproduce el desbordamiento sin avisar.

Ver [[un-guard-sobre-el-minimo-no-acota-la-magnitud]] · [[facturaia]] · [[la-maqueta-se-mide-con-el-motor-no-se-modela-sumando-anchos]].

**Y el censo de dónde está el patrón, a máquina.** El mismo rastreo se hizo a mano tres veces el 8-ago y salieron tres listas distintas (2, 10 y 16), todas incompletas por lo mismo: `<Button[^>]*>` no cruza el `=>` de un `onClick`, así que los botones de varias líneas con manejador inline son invisibles. Hay que cerrar la etiqueta CONTANDO LLAVES. El censo real eran 51. Ver [[un-grep-de-jsx-con-clase-de-caracteres-negada-no-cruza-la-flecha-de-un-onclick]].
