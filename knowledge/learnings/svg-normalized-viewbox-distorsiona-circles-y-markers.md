---
title: svg con viewBox normalizado + preserveAspectRatio none distorsiona circles y markers
date: 2026-04-15
source: claude-code-session
tags: [svg, charts, frontend, responsive]
---

Para charts SVG responsive, la tentación es usar viewBox "0 0 100 100" + preserveAspectRatio="none" para que la curva se estire automáticamente al ancho del contenedor. Funciona para <path> de líneas, pero destruye cualquier <circle> o <rect> con dimensiones fijas: el radio del círculo se escala con factores X≠Y y queda ovalado. vector-effect="non-scaling-stroke" solo preserva el grosor del trazo, no la geometría del elemento.

Solución: medir el contenedor con useLayoutEffect + ResizeObserver síncrono antes del primer paint y usar coordenadas en píxeles reales en el viewBox. Todos los elementos (paths, grids, markers) comparten el mismo sistema de coordenadas y escalan uniformemente.
