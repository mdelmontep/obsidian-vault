---
title: full-bleed de un flex-item con margin negativo (stretch lo agranda)
date: 2026-07-06
source: claude-code-session
tags: [css, layout, flexbox, full-bleed]
---
Para que un hijo de un contenedor flex-column (topbar, banner) se estire "hasta el
borde"/full-bleed sin sacarlo del flujo ni tocar el DOM:

- Con `align-items: stretch` (default), un `margin-left: -Npx` **agranda** el item ese
  ancho (used size = container − margins; margen negativo → crece). Así se desplaza N a
  la izquierda **y sigue llegando** al borde derecho. `-288px` (ancho de la columna del
  sidebar) → cubre de x=0 al borde.
- El contenido NO se mueve compensando el `padding-left` (`calc(col + padding-original)`).
- El ancho de la columna en una **variable** (`--shell-nav-col`) compartida con
  `grid-template-columns`, así el full-bleed sigue cambios de layout sin hardcodear.
- Para pasar "por detrás" de un panel flotante: el panel necesita `z-index` mayor que el
  item estirado (subir el sidebar por encima del topbar/banner). Ver [[modal-portal-stacking-sticky-sidebar]].
- Gatear a desktop (`@media (min-width: 1024px)`): en móvil-drawer no hay columna y el
  margen negativo desborda.
