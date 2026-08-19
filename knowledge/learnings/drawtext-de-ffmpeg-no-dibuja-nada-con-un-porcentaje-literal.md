---
title: drawtext de ffmpeg no dibuja nada con un porcentaje literal, y sale con éxito
date: 2026-08-19
source: facturaia
tags: [ffmpeg, video, escapado, fallo-silencioso]
---
Cuatro trampas de `drawtext`, las cuatro vistas renderizando y ninguna leyendo el código. Medidas en
`node:22-bookworm-slim` con el `ffmpeg` de Debian:

- **El texto en el filtro no se puede escapar bien.** Dentro de `text='…'` ffmpeg NO interpreta escapes:
  un apóstrofo cierra el entrecomillado, la coma del `enable` pasa a separar opciones y muere con
  «Error when evaluating the expression 'gte(t'». Sin comillas y escapando a mano, también falla. Lo
  único que aguanta es `textfile=<ruta>`.
- **Con `textfile`, un `%` literal hace que no dibuje nada y salga con código 0**, sin una línea de
  error: el rótulo desaparece del vídeo. Se apaga con `expansion=none`. Un CTA humano trae `%`, `:` y
  apóstrofos, así que es el caso normal.
- **Sin `fontfile` explícito no hay fuente**: la imagen base no trae ninguna («Cannot find a valid font
  for the family Sans»). En contenedor, copia el `.ttf` dentro.
- **Un `{PLACEHOLDER}` sin sustituir** llega literal y aborta con «No such filter». Calcula el instante
  en el lenguaje anfitrión y pásalo como número.

Gate que discrimina: renderizar sobre **fondo plano** y medir el brillo de la banda del rótulo con
`crop,signalstats` en dos instantes. Sobre `testsrc` la diferencia es 1 punto; sobre negro, 16 → 40.
Ver [[el-arnes-se-mide-a-si-mismo]].
