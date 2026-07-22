---
title: Tooltip sobre botón nativo disabled — necesita pointer-events:none + tabIndex en el wrapper
date: 2026-07-22
source: claude-code-session
tags: [frontend, react, accessibility, tooltip]
---
Un `<button disabled>` nativo no dispara `mouseenter`/`pointerenter` ni deja pasar el hit-test al `<span>` ancestro que lo envuelve — el patrón habitual `<Tooltip><span><Button disabled/></span></Tooltip>` NO abre con el ratón aunque el span esté bien colocado como trigger. Fix: `.btn:disabled { pointer-events: none }` para que el hit-test caiga en el span.

Segundo hueco, más grave, que el primero no cubre: un botón `disabled` tampoco es **focusable**, así que un usuario de teclado no tiene NINGUNA forma de descubrir el motivo del bloqueo (ni con el CSS fix de arriba). Fix: `tabIndex={0}` en el `<span>` wrapper (solo cuando hay contenido de tooltip que mostrar), para que `useFocus`/`aria-describedby` de la librería de tooltip (floating-ui u otra) tenga algo focusable donde enganchar.

Verificar con evidencia real, no visual: `document.querySelectorAll('[role=tooltip]').length` antes/después del hover, y `document.activeElement` tras `agent-browser focus @ref` para confirmar que el foco realmente aterriza en el wrapper. Caso real: TuFacturaIA, botón "Confirmar" de import de recurrentes Holded (PR #1154).
