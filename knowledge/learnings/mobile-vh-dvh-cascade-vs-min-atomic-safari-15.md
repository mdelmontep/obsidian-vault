---
title: mobile — vh/dvh cascada doble declaración, no min() atómico
date: 2026-05-18
source: facturaia FASE 2 mobile polish
tags: [frontend, css, mobile, ios, safari, viewport]
---

Para alturas que deben respetar la URL bar dinámica de Safari iOS, usar `dvh`. Pero Safari <15.4 no soporta `dvh`. Cuando `dvh` va dentro de `min()` o cualquier función CSS, **la función entera se descarta** por sintaxis inválida → la propiedad se queda sin valor → contenedor sin tope.

**OK** (cascada de dos declaraciones):
```css
max-height: calc(100vh - 240px);
max-height: calc(100dvh - 240px);
```

**NO** (atómico — rompe Safari <15.4):
```css
max-height: min(calc(100vh - 240px), calc(100dvh - 240px));
```

Si el valor está en `style={{...}}` inline de React no se puede declarar la propiedad dos veces — mover a clase CSS. Caso real TuFacturaIA: `voz-variables-form.tsx:790` con `min()` atómico → preview de prompt sin scroll en iOS 15.0-15.3.

Ver [[mobile-restore-focus-after-inert-needs-raf]] · [[mobile-inert-plus-aria-hidden-ios-15-fallback]].
