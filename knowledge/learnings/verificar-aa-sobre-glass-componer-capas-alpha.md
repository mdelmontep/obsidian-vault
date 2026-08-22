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

**Y sobre el fondo REAL de la página, no sobre blanco puro** (7-ago): calculé una tinta de marca
y una rampa contra `#ffffff` cuando `--bg` es `#f8f8fa`; al pintarse, 4,35:1 y 2,93:1 — los dos
por debajo del mínimo. Los cazó medirlo en un navegador componiendo con `canvas`, no el cálculo.
Ver [[una-rampa-de-color-validada-contra-el-fondo-no-dice-si-los-pasos-se-distinguen]].

**Y el fondo real puede tener DOS capas, no una** (22-ago): el mismo aviso translúcido se pintaba en dos
sitios — sobre `--bg` en un formulario, y **dentro** de otra caja cuyo fondo era `color-mix(--danger 8%,
--bg-elev)`, con `--bg-elev` también translúcido. La spec de maqueta medía solo la primera y daba verde
para las dos. Regla: la maqueta reproduce el **anidamiento** del componente, no solo su markup, y se
compone de atrás hacia delante (cuerpo → caja → aviso).
Y se comprueba que el caso nuevo **discrimina por su cuenta**: mutando el fondo de la caja intermedia,
el caso anidado tiene que morir y el plano sobrevivir. Si mueren los dos, la mutación no probó nada
del anidamiento; si no muere ninguno, el caso nuevo no mide.
