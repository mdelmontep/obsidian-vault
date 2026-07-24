---
title: escape cierra el modal de más — el culpable no es el popover de floating-ui
date: 2026-07-25
source: claude-code-session facturaia
tags: [frontend, modales, a11y, floating-ui]
---

Si `Modal` escucha `keydown` en `document` y cierra con Escape sin más, el reflejo es culpar al
`<Select>` abierto dentro. **Casi siempre es falso**: `useDismiss` de floating-ui ya hace
`event.stopPropagation()` en su Escape (con `escapeKey.bubbles` por defecto a `false`), así que todo
popover que pase por ahí no filtra.

Los que sí filtran, y hay que buscar estos:
- Popovers con `document.addEventListener('keydown')` **propio** sin `stopPropagation` (dropdowns a
  mano, color pickers, split buttons).
- Popovers portaleados escritos a mano, fuera del hook común.
- **Modales anidados**: si el diálogo de confirmación es él mismo un `<Modal>`, un Escape dispara los
  dos listeners de `document` y cierra el confirm *y* el padre. Esto rompe cualquier guard de
  "¿descartar cambios?" construido sobre ese confirm.
- La ventana de un tick entre abrir el popover y mover el foco dentro (`setTimeout(…, 0)`).

**Fix correcto: pila LIFO de capas en el primitivo**, no `stopPropagation` popover a popover — esa
lista es abierta y se rompe con el siguiente que alguien escriba. Un único listener en `document`;
al recibir Escape, si `defaultPrevented` sale, y si no invoca solo el handler del tope de la pila.
Cada popover/modal se registra al abrir y se desregistra al cerrar.

Relacionado: [[migrar-submodal-a-modal-choca-con-escape-del-contenedor]] ·
[[wcag-2-1-2-no-keyboard-trap-vs-modal-focus-trap]]
