---
title: drawtext no ajusta el texto al ancho, y el ancho se mide con bbox
date: 2026-08-20
source: facturaia
tags: [ffmpeg, video, rotulos, medicion]
---
`drawtext` dibuja al cuerpo que le des: ni envuelve ni encoge. Centrado con `x=(w-text_w)/2`, lo que
sobra se reparte a los DOS lados, así que el rótulo sale cortado por izquierda y derecha y quien mira
no ve que falte algo, ve otro texto. Un CTA de 34 caracteres a cuerpo 42 medía **715 px de un lienzo
de 540** y se leía «balo gratis en tufacturaia.».

- **Se mide con el filtro `bbox`**, no con una regla de caracteres: un fotograma sobre negro y
  `bbox=min_val=40,metadata=mode=print:file=-` escupe `lavfi.bbox.w` a **stdout**. Misma fuente y
  mismo rasterizador que el render final, así que es exacto.
- **`cropdetect` no sirve**: con `limit=0` devuelve el fotograma entero (el negro de vídeo es Y=16,
  no 0) y con `limit=32` dio la medida buena a un cuerpo y basura (`w=-3998`) al siguiente.
- **El ancho es lineal con el cuerpo** (715/518/418 px para 42/30/24, misma cadena): una regla de
  tres da el cuerpo que cabe, sin bisecar renders.
- Orden correcto, el de cualquier editor: PARTIR en líneas equilibradas primero, ENCOGER solo si aún
  no cabe. Y un gate que mire el brillo del CENTRO no discrimina: se enciende igual quepa o no.

Y el ffmpeg de Homebrew **no trae `drawtext`** (sin libfreetype): las pruebas locales salían vacías
sin un solo error y estuve a punto de sacar la constante de esa nada. Se mide en la imagen del runner.
Ver [[drawtext-de-ffmpeg-no-dibuja-nada-con-un-porcentaje-literal]] · [[el-arnes-se-mide-a-si-mismo]].
