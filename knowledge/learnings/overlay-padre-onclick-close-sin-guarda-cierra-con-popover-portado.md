---
title: overlay-padre con onClick=onClose sin guarda cierra el modal al usar un popover portado
date: 2026-06-26
source: claude-code-session
tags: [frontend, react, modal, floating-ui]
---
Modal cuyo backdrop ES el contenedor padre del contenido, con `onClick={onClose}` SIN guarda. Un control que porta su popover a `<body>` (Select/Floating UI con `useClick`) genera un click que burbujea desde el trigger hasta el backdrop-padre → `onClose()` → cierra el modal entero justo al abrir el dropdown. Por teclado NO pasa (ArrowDown abre sin generar click) — por eso parece "solo falla con ratón".

Pista: el resto del modal funciona porque su panel hace `stopPropagation`, pero los submodales montados FUERA de ese panel no quedan protegidos.

Fix: `onClick={(e)=>{ if (e.target===e.currentTarget) onClose() }}` en el backdrop, o montar el backdrop como HERMANO del panel (no padre), como hace el drawer.
Diagnóstico: MutationObserver sobre el overlay + log de pointerdown/click en fase de captura.
Caso real TuFacturaIA #520 (aplicar anticipo). Relacionado: [[zindex-capa-overlay-orden-portal]]
