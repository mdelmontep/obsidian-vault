---
title: la fila que trata Espacio como «abrir» cancela la casilla que lleva dentro
date: 2026-08-19
source: claude-code-session facturaia
tags: [react, accesibilidad, listados, ui]
---

Patrón habitual: una fila con `role="option"` y `tabIndex` que en su `onKeyDown` hace
`if (key === 'Enter' || key === ' ') { preventDefault(); abrir() }`. Si dentro de esa fila vive un
`<input type=checkbox>` de selección múltiple, el Espacio que lo marcaría **burbujea hasta la fila** y
ese `preventDefault()` cancela su activación nativa: con la casilla enfocada no se marca nada. La
selección en lote queda **solo de ratón** y nadie lo nota, porque con el ratón funciona.

Casi siempre el clic YA está resuelto (`onClick` del envoltorio con `stopPropagation`) y al teclado se
le olvidó: buscar el par, no uno de los dos.

Fix: salir del handler cuando el evento no nace en la fila (`if (e.target !== e.currentTarget) return`),
y ponerlo **dentro** de la rama de Enter/Espacio — arriba del handler mata también las flechas, que sí
deben seguir navegando con el foco en la casilla.

Cómo se ve, sin adivinar: sonda en el navegador con dos escuchas, una en el input y otra en
`document`. Si llega `defaultPrevented: false` al input y `true` a `document`, alguien lo cancela en
medio del camino. Ver [[una-suite-en-verde-no-prueba-el-camino-real]].
