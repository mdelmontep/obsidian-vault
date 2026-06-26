---
title: tabla densa → tarjeta en móvil — celdas estrechas heredan el ellipsis del td y display:flex en td rompe colSpan
date: 2026-06-26
source: claude-code-session
tags: [frontend, css, mobile, responsive, table]
---

Al colapsar una `<table>` densa a tarjetas en móvil (patrón `fact-table` de facturaia):

- **`text-overflow:ellipsis` en el `td` genérico pinta "…" sobre hijos NO-texto** (checkbox, badge) si la caja de contenido (width − padding) es más estrecha que el hijo. Pasa también en el `<th>`. Fix: `overflow:visible; text-overflow:clip` en esas columnas (col-chk/col-vf/col-estado) o bajar su padding. Caso: checkbox 18px en col-chk de 36px con padding 0 12px → caja 12px → "…".
- **No uses scroll horizontal para "ver todas las columnas" en móvil.** Mejor disclosure inline (chevron que despliega los campos ocultos en una línea extra); el tap-fila sigue abriendo el detalle. Sin columnas nuevas → reutiliza una celda existente con `display:none` en desktop, así `colSpan` no cambia.
- **`display:flex` en un `<td>` lo saca del layout de tabla y rompe el `colSpan`** de filas cabecera (mes/totales) en DESKTOP. Acótalo al `@media` móvil donde el `<tr>` ya es `display:block`. Para empujar sumas a la derecha en estrecho usa flex + `margin-left:auto`, no `float:right` (el float deja que el texto inline se le monte encima).

Ver [[mobile-overflow-layout-viewport-contain-y-grid-span]] · [[pill-overflow-hidden-en-grid-se-recorta-usar-container-query-en-modal]].
