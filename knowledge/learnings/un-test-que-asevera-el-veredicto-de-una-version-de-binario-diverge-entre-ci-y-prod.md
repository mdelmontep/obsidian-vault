---
title: un test que asevera el veredicto de una versión de binario diverge entre CI y prod
date: 2026-09-15
source: agh-iberica
tags: [testing, ci, docker, versiones]
---
Un binario del sistema (qpdf, poppler, ffmpeg, ImageMagick…) no trae la misma versión en cada sitio. Lo instala el apt del runner de CI, el apk de la imagen de prod y Homebrew en el portátil, cada uno con la suya.

Caso real (agh-iberica #1762): con un PDF dañado, qpdf 12.x (alpine en prod, Homebrew en local) sale con exit 2 y 11.9 (Ubuntu en Actions) recupera el documento con exit 3. El test fijaba `tool_failed`: verde en local, rojo en CI. Local coincidía con prod por casualidad.

- **Asevera la propiedad y no el veredicto de una versión:** «no es `tool_missing`», o «es uno de `[ok, tool_failed]`».
- **Si la conducta importa de verdad:** el job de CI corre dentro de la misma imagen base que prod (`container:` en el job), o el test lee `--version` y falla con un mensaje claro si la serie no coincide (agh-iberica #1765).
- **Síntoma que lo delata:** rojo solo en CI, en un test de un binario, sin tocar ese código.
