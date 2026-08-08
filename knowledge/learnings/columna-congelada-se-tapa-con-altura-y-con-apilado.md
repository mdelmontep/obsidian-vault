---
title: una columna congelada se tapa con altura Y con apilado, y las dos fallan por separado
date: 2026-08-08
source: claude-code-session
tags: [css, frontend, accesibilidad, sticky, z-index]
---

Celda `position: sticky` en una rejilla que scrollea en horizontal. Dos fallos
distintos que hay que arreglar juntos, y el segundo no se ve:

1. **Altura.** Si la fila centra sus celdas (`align-items: center`), la celda
   fijada mide lo que su contenido, no lo que la fila: un tic de 18 px en una
   fila de 37 deja dos bandas por las que se ve pasar lo que se desplaza, y el
   tapón `::before` con `top:0;bottom:0` hereda esa altura corta. Se arregla con
   `align-self: stretch`, no subiendo el `z-index`.
2. **Apilado.** El `z-index` de un PRIMITIVO compite en el contexto de
   apilamiento del CONTENEDOR. El `<input>` real de un Checkbox va en `z-index:
   2` para ganar a su propio recuadro pintado, y eso basta para que los tics de
   las columnas desplazadas queden por encima de la columna congelada. Como el
   input es `opacity: 0`, no se ve: **captura el clic**. Se acota con
   `isolation: isolate` en la fila, que encierra ese 2 sin que la fila suba por
   encima de la cabecera pegajosa.

El síntoma visible era un jirón de dos píxeles; el daño real era que pulsar la
casilla de seleccionar marcaba el tic de mano de obra de esa línea y le movía el
precio. Se descubre con `document.elementFromPoint(x, y)` sobre el control fijado
a varios `scrollLeft`, nunca mirando una captura. Un test que fije el número del
primitivo a mano no sirve: hay que leerlo de su `.module.css`.

TuFacturaIA #1543 (ticket 144). Relacionado: [[zindex-capa-overlay-orden-portal]] ·
[[el-objetivo-tactil-de-un-control-compuesto-es-su-hijo]]
