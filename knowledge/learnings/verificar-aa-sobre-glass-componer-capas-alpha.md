---
title: verificar aa sobre superficies translucidas componiendo capas alpha en script
date: 2026-06-10
source: claude-code-session
tags: [a11y, css, contraste, glassmorphism]
---
Contraste WCAG sobre glass/translúcidos no se mide contra un color: se mide contra el **compuesto**
de capas. Script node ~30 líneas: alpha-compositing sRGB capa a capa (peor fondo → scrim → panel →
velo del body) y ratio WCAG del texto sobre el resultado. Aproximación sRGB válida para
`color-mix(in oklch, C X%, transparent)` a efectos de pasa/no-pasa.

Claves:
- Distinguir **peor caso teórico** (imagen/PDF sólido extremo detrás, solo plausible con lightboxes)
  de **fondo real de la app** (--bg + tablas). Reportar ambos; decidir sobre el real, mitigar el teórico.
- El knob correcto es el **velo del contenido scrollable** (`bg-elev` 30→38%), no la opacidad del panel
  (doc §3 glassmorphism: cristal y texto desacoplados).
- Si un token falla también sobre fondo sólido (ej. danger small-text 3.5:1) es baseline pre-existente
  de la app, no regresión del glass — no "arreglarlo" tocando el glass.
