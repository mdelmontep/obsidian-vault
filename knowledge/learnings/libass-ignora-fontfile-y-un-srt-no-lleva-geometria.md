---
title: libass ignora fontfile, y un .srt no lleva geometría
date: 2026-08-20
source: facturaia
tags: [ffmpeg, video, subtitulos, fallo-silencioso]
---
Quemar subtítulos con ffmpeg no es `drawtext` con otro texto: los pinta **libass** (filtro
`subtitles`) y no comparte ninguna de sus opciones. Dos fallos silenciosos, los dos vistos
extrayendo un fotograma y **mirándolo**:

- **No existe `fontfile` para `subtitles`.** libass resuelve SIEMPRE por fontconfig y `fontsdir` no
  basta: con `force_style=FontName=Filson Soft` pedía la familia buena y fontconfig devolvía
  `DejaVuSans.ttf` (`fontselect: (Filson Soft, 400, 0) -> …`). Sale con éxito y el vídeo va con otra
  tipografía. Fix en contenedor: `cp *.ttf /usr/share/fonts/truetype/<x>/ && fc-cache -f`. DejaVu
  entra como dependencia de ffmpeg, y por eso no se nota: hay fuente, no es la tuya.
- **Un `.srt` no lleva geometría.** ffmpeg lo convierte con una cabecera ASS por defecto de
  `PlayRes 384×288` y libass escala a la resolución real: en 1080×1920 todo se multiplica ×3,3 y el
  rótulo sale gigante y arriba. Genera `.ass` con el tamaño del vídeo como PlayRes.

En ASS, además: `BorderStyle=3` pinta la caja con **OutlineColour** (BackColour es la sombra), los
colores son `&HAABBGGRR` (BGR, y el alfa es transparencia) y un `Dialogue` con un campo de más mete el
separador dentro del texto. Ver [[drawtext-de-ffmpeg-no-dibuja-nada-con-un-porcentaje-literal]] ·
[[el-arnes-se-mide-a-si-mismo]].
