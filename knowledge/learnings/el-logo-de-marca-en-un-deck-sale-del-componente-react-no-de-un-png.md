---
title: el logo de marca en un deck sale del componente react, no de un png
date: 2026-09-22
source: facturaia
tags: [artifacts, slides, marca, svg]
---
Un deck de Artifact Slides sobre lienzo fijo (1920×1080) admite `<svg>` inline hasta ~52 KB por
diapositiva, así que el logo del producto no hay que rasterizarlo: se extraen los `<path>` del
componente React que ya lo pinta (`src/components/layout/logo.tsx`) y se inlinean por diapositiva.

Cómo, en facturaia:
- Isotipo y wordmark tienen viewBox propios (`0 0 309.02 471.31` y `0 0 1445.37 175.58`) y una
  proporción de altura fija (`WORDMARK_HEIGHT_RATIO`): respetarla o el logo sale descompensado.
- El fill del cuerpo es `currentColor` y el acento `var(--logo-accent)` (`#8FB8F9`, `tokens.css`).
  En el script generador se sustituye el fill por un parámetro → tinta oscura en las diapositivas
  claras, blanco sobre la de marca. Un PNG no permite eso.
- Los paths de sombra con gradiente se descartan: no aportan a 1920 px y se comen el presupuesto.

Ventaja real: escala sin bordes, recolorea por diapositiva y no gasta asset store.
