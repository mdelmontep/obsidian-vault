---
title: css grid `1fr` a secas desborda — usa `minmax(0,1fr)` en tracks flexibles
date: 2026-06-10
source: claude-code-session
tags: [css, grid, overflow, layout]
---
`1fr` equivale a `minmax(auto,1fr)`: el track nunca encoge por debajo del min-content de su contenido. Si la celda contiene una tabla/lista con columnas de ancho fijo cuyo min-content supera el espacio libre, el grid desborda el contenedor padre y el contenido se corta fuera del viewport.

Fix en dos patas:
1. `minmax(0, 1fr)` en el track flexible — permite que encoja.
2. `overflow-x: auto` en el scroller interno — red de seguridad: scroll horizontal contenido en vez de romper el layout.

Si la fila interna también es grid, sustituir anchos fijos por `minmax(min, fr)` por columna para que degrade gracefully.

Caso real (TuFacturaIA detalle 303, PR #177): fila de facturas con min-content ~710px en columna de ~652px → importes cortados. Tema hermano (viewport móvil): [[mobile-overflow-layout-viewport-contain-y-grid-span]].
