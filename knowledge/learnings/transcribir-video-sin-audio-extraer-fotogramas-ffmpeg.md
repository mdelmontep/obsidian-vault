---
title: no puedo transcribir audio, pero sí leer un vídeo por fotogramas con ffmpeg
date: 2026-07-17
source: claude-code-session
tags: [video, ffmpeg, ocr, workflow]
---
Cuando alguien manda un vídeo (demo de una app, tutorial) NO hay tool para oír
el audio ni transcribir voz. Pero lo que se VE en pantalla sí se puede leer:

```
ffmpeg -v error -i video.mp4 -vf "fps=1/5,scale=1280:-1" -q:v 4 out/f_%03d.jpg
```

Extrae 1 fotograma cada 5s escalado, y luego Read de los .jpg (pasada gruesa
cada ~4 frames, luego zoom a los que tengan datos). Suficiente para menús,
campos, números, flujo de clics. Para el audio: pedir transcripción externa
(.txt) o que lo cuenten por texto. Caso real: 2 vídeos de WAPI de Natalia →
confirmé fórmula de precios y catálogo MO solo con lo visible, sin audio.
Ver [[importar-csv-erp-espanol-encoding-cp1252-y-precio-por-unidad-multiple]] ·
[[agent-browser-screenshot-cuelga-apps-con-polling]].
