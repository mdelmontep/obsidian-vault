---
title: chrome headless no sirve para probar scroll móvil: mínimo 500 px y no captura el scroll del iframe
date: 2026-10-15
source: agentesia-lab (presentación Orión Dental)
tags: [testing, chrome, mobile, frontend]
---
- `--headless --window-size=375,...` no baja de unos 500 px de ancho. Si se envuelve la página en un iframe de 375 px, `--screenshot` no refleja el `scrollTo` hecho dentro del iframe: sale siempre el hero.
- Lo que funcionó: `python3 -m http.server --directory <dir>` (mismo origen) + una página envoltorio con `<iframe width=375>`, abierta en Chrome real (Claude in Chrome). Con `javascript_tool` se hace scroll en `f.contentWindow` y se comparan los estados (`dataset`, `.on`) contra la posición: los números delatan el desfase y la captura lo confirma.
- Gotcha: con `scroll-behavior:smooth` en `html`, un `scrollTo` seguido de una lectura inmediata da posiciones a medio camino → poner `scrollBehavior='auto'` antes de medir.
- Relacionado: [[intersectionobserver-ignora-rootmargin-dentro-de-un-iframe]].
