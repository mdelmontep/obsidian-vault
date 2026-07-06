---
title: un panel glass flotante necesita fondo detrás para no verse plano (+ liquid glass portable)
date: 2026-07-06
source: claude-code-session
tags: [css, glassmorphism, liquid-glass, backdrop-filter]
---
`backdrop-filter` sobre un fondo plano/vacío = cristal plano, "pegado". Un panel glass
(sidebar flotante) sobre la celda desnuda del grid no refracta nada.

- **Fix**: que el mesh/gradiente de fondo pase POR DETRÁS del panel (extender el fondo,
  no cortarlo donde empieza el panel), y subir el panel a `z-index` mayor que ese fondo
  fijo para muestrearlo. El cristal toma su color del fondo — ese es el efecto.
- **Liquid Glass (iOS 26) portable**: la versión completa (SVG `feDisplacementMap` como
  input de `backdrop-filter`) es **solo Chrome** — no usar en SaaS multi-navegador. El
  subset robusto: `backdrop-filter: blur+saturate` + capa de **specular highlight**
  (gradiente de luz en borde sup-izq, como `background-image`, NO pseudo, para no tocar
  z-index de hijos) + rim de luz `inset 0 1px 0` + sombra en capas (nunca sombra plana
  única → "parece IA").
- Prefijo `-webkit-backdrop-filter`: lo pone el build (lightningcss); a mano lo colapsa.
- Contraste sobre glass: ver [[verificar-aa-sobre-glass-componer-capas-alpha]].
