---
title: "borde con luz que orbita: conic + @property --angle, y acelerar en hover sin salto con WAAPI playbackRate"
date: 2026-07-17
source: claude-code-session
tags: [css, animation, frontend, glassmorphism]
---
Borde animado con una perla de luz recorriéndolo (dropzone premium):
- El anillo es `conic-gradient(from var(--a), ...)` recortado al borde con máscara
  (`mask-composite: exclude` + padding). Para GIRAR no sirve `transform: rotate` (la máscara
  se queda fija); hay que animar el ángulo: `@property --a {syntax:'<angle>'}` +
  `@keyframes { to { --a: 360deg } }`. Costura invisible ⇒ extremos del gradiente transparentes.
- Cola sin corte: pon el punto brillante lejos del 0/360 y una cola que se funde gradual.
- Acelerar al hover SIN que la perla salte de sitio: NO cambies `animation-duration`
  (recalcula la fracción del keyframe → salto). Usa Web Animations API en JS:
  `el.getAnimations().forEach(a => a.updatePlaybackRate(2.4))` (conserva currentTime, rampa suave).
- Halo de cristal que crece de 0: `backdrop-filter` + máscara radial para bordes difusos
  (no `border-radius` duro); necesita textura detrás que difuminar
  ([[glass-flotante-necesita-fondo-detras-liquid-glass-portable]]). Respeta `prefers-reduced-motion`.
