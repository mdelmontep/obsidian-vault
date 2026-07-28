---
title: un clic por coordenadas tras un salto de layout no cae en el botón, y parece un bug del botón
date: 2026-07-28
source: claude-code-session
tags: [testing, navegador, cls, debugging]
---

Al conducir el navegador, clicar por `coordinate` usa la posición de una captura
anterior. Si entre la captura y el clic la página se desplaza (CLS, un banner que
aparece, una imagen que carga), el clic cae al lado: **no pasa nada, no hay
error, no sale ninguna petición**. Es indistinguible de un botón roto.

Caso real (TuFacturaIA, `/fiscal/.../303/2T`): estuve a punto de dar por
reproducido "el botón no dispara ninguna petición". Repetido con `find` +
`ref`, el mismo botón respondió `200` a la primera. Y el síntoma original que
llevaba semanas sin explicación encaja con esto: la app tiene un CLS conocido
en `.billing-banner`, que empuja el contenido en todas las páginas.

**Regla**: en smokes de navegador, clicar por referencia de elemento (`find` →
`ref`), nunca por coordenadas, salvo que no haya alternativa. Y si un clic "no
hace nada", descartar primero que haya caído fuera antes de acusar al código.

Ver [[cero-mientras-carga-no-es-cero-vacio-y-provoca-cls]].
