---
title: agent-browser fill con cadena vacía no dispara el onChange de React
date: 2026-08-13
source: claude-code-session
tags: [agent-browser, react, smoke, e2e]
---

`agent-browser fill @ref ""` sobre un input/textarea controlado de React deja
el campo visualmente vacío pero **no dispara `onChange` con el valor vacío**:
el estado del componente conserva el valor anterior, el botón de guardar
refleja un estado que no es el del DOM, y el guardado persiste el dato viejo
sin ningún error. Con texto no vacío, `fill` funciona bien.

Fix para vaciar un campo controlado: hacerlo por teclado —
`click @ref` → `press Meta+a` → `press Backspace` (o `type @ref "x"` +
`press Backspace`) — y verificar la persistencia contra el backend (BD o
respuesta de red), nunca contra el aspecto del campo.

Caso: vaciar `copy_publicacion` en el smoke de contenido-06 (facturaia,
13-ago-2026): dos "guardados" en verde que no habían guardado nada; el PATCH
real solo salió tras vaciar por teclado.
