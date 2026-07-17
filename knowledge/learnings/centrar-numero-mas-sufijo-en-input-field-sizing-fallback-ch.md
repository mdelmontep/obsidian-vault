---
title: centrar número+sufijo dentro de un input como unidad — field-sizing:content con fallback en ch
date: 2026-07-18
source: claude-code-session
tags: [css, frontend, forms, safari]
---
Stepper/casilla con `<input>` + sufijo ("días", "€", "%") dentro de una caja
flex con `justify-content:center`: si el input lleva `width:100%` llena la
caja, el dígito se centra en TODO el ancho y el sufijo queda pegado al borde;
con 2-3 cifras el número llega a solaparse con el sufijo. Nunca se leen como
un grupo centrado.

Fix: el input debe medir su contenido, no el contenedor.
- Base robusta: `width: <N>ch` fijo que aguante el valor máximo (p.ej. 3.2ch
  para "180") — funciona en TODOS los navegadores.
- Mejora: `@supports (field-sizing: content) { width:auto; field-sizing:content;
  min-width:1ch; max-width:4ch }` → ancho exacto al contenido en Chrome/Edge/FF.

Clave: **Safari aún NO soporta `field-sizing`** (jul-2026) → sin el fallback en
`ch`, en Safari el número se recorta. Poner siempre la base fija primero.
Caso real: steppers de cadencia del Agente de cobros (TuFacturaIA, PR #989).
