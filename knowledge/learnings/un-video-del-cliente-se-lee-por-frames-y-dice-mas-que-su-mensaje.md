---
title: un vídeo del cliente se lee por frames, y dice más que el mensaje que lo acompaña
date: 2026-08-02
source: claude-code-session
tags: [metodo, clientes, requisitos, ffmpeg]
---
Natalia mandó 3:27 grabando su ERP viejo con una frase: «poder abrir desde el
presupuesto una unidad de obra y otra después». El vídeo traía tres cosas que la
frase no decía, y las tres cambiaban el diseño: eran **tres** saltos y no uno
(presupuesto → unidad → anidada → ficha del material), todo abría en **consulta**
con un botón «Modificar» aparte (o sea, la pregunta de producto que iba a hacerle
ya estaba contestada), y hacía falta un requisito previo que no estaba en el issue
(dirección propia para la unidad, hoy es un modal).

Cómo leerlo, sin transcriptor de audio local:
```bash
ffmpeg -i v.mp4 -vf "fps=1/10,scale=848:-1" -q:v 3 f_%03d.jpg   # mapa: 1 cada 10 s
ffmpeg -ss 42 -i v.mp4 -vframes 1 -vf "crop=280:200:180:180,scale=1120:-1" z.jpg
```
El `crop`+`scale` del segundo es lo que deja leer un menú de 9 px fotografiado con
el móvil. Y avisa de lo que el cursor tapa: en un enlace del globo se leía
`Consultar U.Obra Pre…` en todos los fotogramas. Eso se reporta como pregunta, no
como dato. Ver [[antes-de-preguntar-al-cliente-mira-si-el-dato-esta-en-el-sistema-origen]].
