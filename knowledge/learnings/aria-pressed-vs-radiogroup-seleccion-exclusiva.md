---
title: aria-pressed modela toggle independiente, no exclusión mutua
date: 2026-05-18
source: claude-code-session
tags: [a11y, aria, apg, react]
---

W3C APG: selección exclusiva entre N opciones (segmented control, doc-tabs, filter chips de estado) = `role="radiogroup"` + `role="radio"` + `aria-checked` + roving tabindex + flechas izq/der/Home/End.

`aria-pressed` es para toggles binarios INDEPENDIENTES (Bold, Pin, Mute). En grupo exclusivo, NVDA/JAWS lee 4 toggles separados, no "1 de 4". Radix ToggleGroup `type="single"` mapea a radiogroup precisamente por esto.

Botones con texto descriptivo NO necesitan `aria-label` adicional — el contenido es el accessible name. `aria-label` SÍ en el contenedor radiogroup.

`role="tab"` requiere `tabpanel` asociado + `aria-controls` — sin paneles distintos no es tabs, es radiogroup.

Ver [[scroll-shadows-komarov-con-css-variable-dark-mode]] · APG: https://www.w3.org/WAI/ARIA/apg/patterns/radio/
