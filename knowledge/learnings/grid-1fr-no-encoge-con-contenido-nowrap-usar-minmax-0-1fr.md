---
title: un track de grid 1fr no encoge bajo su contenido nowrap; usar minmax(0, 1fr)
date: 2026-07-15
source: claude-code-session
tags: [css, grid, overflow, responsive, movil]
---
`grid-template-columns: 1fr` da un track con `min-width: auto` = min-content. Con
contenido `white-space: nowrap` (título, badge) el min-content supera el viewport y
el track NO encoge → la columna desborda y el elemento de la derecha (badge, importe)
se sale, aunque el hijo interno tenga `min-width:0` + ellipsis.

Fix: `grid-template-columns: minmax(0, 1fr)` (permite bajar de min-content y fuerza
truncado) + `min-width:0` en la cadena de contenedores flex-column anidados.

Caso real (TuFacturaIA móvil PR5): `.ingesta-body` grid 2-col; en móvil el track `1fr`
no encogía por el título nowrap → badge fuera de pantalla. Lo caza el QA visual, no el
build (compila perfecto). Un flex-column simple (no grid) no sufre esto. Ver [[facturaia]].
