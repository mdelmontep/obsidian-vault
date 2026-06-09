---
title: overflow móvil — el layout viewport se expande (contain:layout) y grid-column span crea columna implícita
date: 2026-06-10
source: claude-code-session
tags: [frontend, css, mobile, overflow, grid]
---

Tres causas de "página descuadrada/encogida" en móvil, NO detectables a ojo. Medir en browser: `window.innerWidth` vs `document.body.scrollWidth` vs `window.scrollX`.

- **`grid-column: span 2` en un grid colapsado a 1 col (mobile) crea una 2ª columna implícita** y ensancha el grid fuera del viewport. Fix: `grid-column: 1 / -1` (ancho completo en 1 y 2 cols, sin track implícito). Añadir `min-width:0` en la cadena flex/grid.
- **`display:inline-flex` como item de un flex en columna se dimensiona a su contenido**, no al contenedor → su propio `overflow-x:auto` nunca scrollea y empuja la página. Fix: `display:flex; min-width:0; max-width:100%`.
- **Un `overflow-x:auto` cuyo contenido excede su scroll-box expande el LAYOUT VIEWPORT móvil** (`innerWidth` crece, todo "encoge para caber"). `overflow:clip` en ancestros NO lo arregla. Fix: `contain: layout` en el contenedor scrollable (aísla el subárbol; el scroll interno sigue). Overlays/popovers deben ir por `createPortal` o `contain` los recorta.

Diagnóstico clave: `pageScrollX=0` pero `innerWidth>vw` = viewport de layout expandido, ≠ scroll de página (los `fullPage` screenshots engañan). Caso facturaia PR #161 (/generar, /emitidas, /recibidas). Ver [[mobile-table-scroll-x-needs-region-tabindex-wcag-2-1-1]].
