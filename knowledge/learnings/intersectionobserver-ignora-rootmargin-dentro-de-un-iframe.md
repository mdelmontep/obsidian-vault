---
title: intersectionobserver ignora rootmargin dentro de un iframe y desincroniza el scroll narrativo
date: 2026-10-15
source: agentesia-lab (presentación Orión Dental, artifact de claude.ai)
tags: [frontend, scroll, iframe, artifacts]
---
- Síntoma: en el artifact publicado (claude.ai lo sirve en un iframe), el paso activo iba 1-2 por delante del texto. En local, abriendo el HTML suelto, iba bien.
- Causa: con raíz implícita, la raíz es el viewport de la ventana de nivel superior, no el del iframe. Si el iframe es de otro origen, el `rootMargin` se ignora; si es del mismo origen, la banda se mide contra la ventana de fuera. Así, un `rootMargin:'-50% 0px -40% 0px'` deja de ser una línea de lectura y el último elemento que entra gana.
- Fix: en el `scroll` (con rAF), quedarse con el último elemento cuyo `getBoundingClientRect().top <= innerHeight*f`. Son pocos elementos, así que es barato y funciona igual dentro y fuera del iframe.
- Sirve para cualquier página que se embeba (artifacts, widgets, previews). El `IntersectionObserver` sigue valiendo para los reveals de «entra/sale», no para elegir un único elemento activo.
- Probarlo dentro de un iframe del tamaño real; ver [[chrome-headless-no-sirve-para-probar-scroll-movil-en-iframe]].
