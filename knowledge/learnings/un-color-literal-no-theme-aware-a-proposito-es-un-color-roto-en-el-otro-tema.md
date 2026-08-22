---
title: un color literal «no theme-aware a propósito» es un color roto en el otro tema
date: 2026-08-22
source: facturaia
tags: [css, dark-mode, accesibilidad, gotcha]
---

Un comentario que dice «literales a propósito, para no cambiar el resultado en dark» está declarando
que el otro tema **no se miró**. Preservar el comportamiento incluye preservar el fallo.

Caso real (TuFacturaIA, #2091): la insignia de divisa pintaba `#1B2B4B` sobre
`rgba(61,123,245,0.10)`. En claro, 11,0:1. En oscuro, el fondo translúcido se compone sobre
`#0B1428` y da `rgb(16,30,60)`: contraste **1,1:1**, invisible. Vivió meses porque casi todas las
filas enseñaban la variante ROJA (`manual_requerido`), que sí se distingue; al arreglar el bug de
fondo, la azul pasó a ser la normal de 118 filas y el fallo saltó a la vista.

- **Un arreglo que cambia qué variante es la habitual destapa el contraste de la variante nueva.**
  Al cambiar el estado por defecto de algo, mirar sus colores en los dos temas.
- Medir en la página real, no a ojo: `getComputedStyle` + componer el `rgba` sobre el fondo del
  `body` da el ratio de verdad. Un translúcido no se evalúa contra sí mismo.
- El arreglo no es tocar el tema claro: es dar al oscuro **su propio juego**, y ahí con tokens
  (`--brand-fg`, `--danger-fg`, `--text-2`) ya calibrados, no con más literales.

Primo de [[css-background-white-hardcoded-rompe-dark-mode-silencioso]], pero al revés: allí el fondo,
aquí el texto, y aquí con una justificación escrita que lo hacía parecer decidido.
