---
title: popover dentro de modal con overflow hidden se corta usar inline disclosure
date: 2026-04-28
source: claude-code-session
tags: [frontend, css, modal]
---

Popover con `position: absolute` dentro de un modal con `overflow: hidden` (típico para `border-radius`) queda **clipado** por el ancestro. El popover se renderiza pero solo se ve la parte que cae dentro del modal-body. En móvil casi no se ve.

## Soluciones

1. **Inline disclosure** (mejor en la mayoría de casos): el popover NO es flotante, es un `<div>` siguiente que se expande en el flujo cuando se abre. Empuja el contenido. Sin clipping, mejor en móvil, sin re-posicionar al hacer scroll, accesible por defecto.
2. **Portal con position fixed**: render via React portal a `document.body`, posición fija calculada con `getBoundingClientRect` del trigger. Más complejo, hay que actualizar al scroll/resize.

## Trade-off

Inline empuja contenido (puede saltar el preview o el footer del modal). Si el contenido del popover es grande, esto es preferible — entras en modo "configurar" sin distracciones flotantes. Si es pequeño (1-2 items), portal es más natural.

FacturaIA usó inline para el picker de tokens del builder de series.
