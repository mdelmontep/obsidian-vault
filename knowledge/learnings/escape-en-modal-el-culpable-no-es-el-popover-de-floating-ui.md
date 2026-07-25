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

**COROLARIO (2026-07-25, encontrado dogfoodeando, no leyendo): durante la migración la pila protege
menos de lo que parece.** No puede hacer `stopPropagation` (dejaría sordos a los overlays que aún
escuchan en `window`, que en el burbujeo van DESPUÉS de `document`), y `preventDefault()` **no para a un
listener HERMANO del mismo nodo**. Si ninguno de los no migrados comprueba `defaultPrevented` —cosa que
hay que verificar, no suponer— un overlay con listener propio que esté **DEBAJO** de una capa de la pila
se cierra con el mismo Escape: un Escape, dos capas. Es el bug original en dirección contraria.
Por eso la lista de pendientes se prioriza por «¿puede tener un `<Modal>` encima?», no por orden
alfabético: ahí están los pares alcanzables (un `confirm()` sobre el detalle de factura cerraba la
factura con la edición en curso). Y la lista canónica vive en UN sitio, el propio módulo de la pila:
dos listas en dos ficheros dieron 8 y 8 sin solaparse cuando el grep real daba 21.

Relacionado: [[migrar-submodal-a-modal-choca-con-escape-del-contenedor]] ·
[[wcag-2-1-2-no-keyboard-trap-vs-modal-focus-trap]]
