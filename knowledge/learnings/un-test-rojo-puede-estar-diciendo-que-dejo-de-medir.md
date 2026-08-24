---
title: un test rojo puede estar diciendo que dejó de medir, no que el código esté mal
date: 2026-08-24
source: panel-tecnocloud
tags: [testing, fixtures, mutacion, seguridad]
---

Un caso de integración creaba un adjunto `image/png` y esperaba `application/octet-stream`
(la defensa anti-XSS: lo que no está en la allowlist se fuerza a descarga). El handler había
cambiado de decidir por un **flag** a decidir por **MIME contra allowlist**, y el png está en la
allowlist: el test se puso rojo.

- El arreglo obvio —actualizar la expectativa al nuevo valor— deja el caso **verde y vacío**: su
  fixture ya no cae en la rama que dice cubrir. Lo correcto es mover el FIXTURE de vuelta a la
  rama (aquí, un `application/pdf`), no rebajar el aserto.
- Regla: cuando una condición pasa de mirar un flag a mirar una lista, **todo fixture que esté en
  la lista deja de ejercitar la rama del else**, y el rojo es el único aviso que te llega.
- Compruébalo por mutación, que es lo que distingue un caso de otro: romper la reescritura del
  handler mataba **1** caso antes y **2** después.
- Y salió al correr la suite por primera vez en meses: **una suite fuera del gate se pudre en
  silencio**. Aquí no hacía falta Docker, bastaba el Postgres de brew.

Espejo de [[test-verde-puede-codificar-el-bug-como-esperado]].
