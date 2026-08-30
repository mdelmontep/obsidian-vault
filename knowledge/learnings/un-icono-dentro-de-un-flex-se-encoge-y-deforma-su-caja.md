---
title: un icono dentro de un flex se encoge y deforma su caja sin que nada avise
date: 2026-08-30
source: facturaia
tags: [css, flexbox, iconos, frontend]
---
Un `<svg>` con `width`/`height` fijos NO conserva su tamaño dentro de un flex: el
`flex-shrink: 1` de fábrica le come el ancho cuando el contenedor va justo, y como el alto
no se toca, la caja sale **rectangular**. No hay warning, no hay overflow, no hay nada que
mirar: el icono simplemente está mal proporcionado y se lee como «diseño descuidado».

Medido el 30-ago-2026 en TuFacturaIA: el aspa de los banners salía a 10×12 y el chevron de
plegar el menú a 10×16, con `size` pedido de 16.

- Fix: `svg.lucide { flex: none }` — **por elemento**, no en el botón concreto. Lucide estampa
  `class="lucide"` en cada svg que dibuja, así que la regla vale también donde mañana alguien
  meta el icono en otro flex. Con `<img>` es el mismo problema y el mismo remedio.
- Cómo se caza: medir `getBoundingClientRect()` de todos los svg de la página y agrupar por
  `WxH`. Cualquier caja que no sea cuadrada, o que no esté en la escala, es un candidato.
  A ojo no se ve; en una tabla de tamaños salta a la primera.
- Ver [[flexbasis-en-flex-direction-column-se-interpreta-como-alto]].
