---
name: wcag-2-1-2-no-keyboard-trap-vs-modal-focus-trap
description: Confusión WCAG 2.1.1/2.1.2 — en modals/drawers el foco DEBE atraparse dentro (cicla Tab) y permitir salida solo con Escape.
date: 2026-05-22
source: claude-code-session
tags: [a11y, wcag, modal, focus, frontend]
---

**Confusión común**: WCAG 2.1.1 "Keyboard" dice "todo accesible por teclado" y 2.1.2 "No Keyboard Trap" dice "no atrapar foco indefinidamente". Muchos devs interpretan que en modals NO deben atrapar el foco → bug.

**La regla correcta para modals/drawers** (ARIA Authoring Practices Guide):
1. Al abrir: foco va al primer elemento focusable (o botón cerrar) dentro del modal
2. **Tab/Shift+Tab CICLA** primer↔último focusable DENTRO del modal — no escapa al fondo
3. Escape SÍ cierra el modal (mecanismo estándar de salida — cumple 2.1.2)
4. Al cerrar: foco vuelve al elemento que abrió el modal

**Bug típico** (que no atrapa Tab): solo enfocan el botón cerrar al abrir + restauran foco previo al cerrar, pero Tab puede escapar al `<body>` mientras el modal está abierto → usuario teclado pierde contexto + screen reader lee fondo.

**Patrón fix**: hook `useFocusTrap(ref, open)` que captura `keydown` Tab/Shift+Tab, identifica `[tabindex]:not([tabindex="-1"]), button:not([disabled]), input, ...` dentro del ref, y cicla. Reusable en cualquier modal/drawer.

Validable con keyboard nav real (Tab repetido sin ratón), no con linter automático.
