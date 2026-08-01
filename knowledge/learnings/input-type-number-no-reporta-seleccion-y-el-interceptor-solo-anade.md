---
title: input type=number no reporta selección, así que un interceptor de beforeinput solo sabe añadir
date: 2026-08-01
source: claude-code-session
tags: [frontend, react, forms, inputs, regresion]
---
`<input type="number">` NO implementa la Selection API: `selectionStart`/`selectionEnd` son SIEMPRE
`null` (spec HTML, los tres navegadores), y `setSelectionRange` lanza `InvalidStateError`. Si
interceptas `beforeinput` para sanear lo tecleado y calculas el rango con
`input.selectionStart ?? raw.length`, ese fallback es la ÚNICA rama que se ejecuta nunca: seleccionar
todo y escribir encima CONCATENA (33 + "7" → 337) y Backspace con todo seleccionado borra un carácter.
Con `preventDefault()` incondicional, el reemplazo que el navegador sí sabía hacer tampoco ocurre.

Fix: que el nodo sea `type="text"` MIENTRAS tiene el foco (+ `inputMode="decimal"` para el móvil) y
vuelva a `number` al soltarlo. Tres cabos obligatorios: reponer el stepping con ↑/↓, sostener
`min`/`max` a mano con `setCustomValidity` (también AL ENFOCAR), y contar con que React reescribe
`type` en cada commit.

Y el que se cuela: tras el `dispatchEvent('input')` React encola un "restore de estado" del input
controlado que corre DESPUÉS del `useLayoutEffect` y devuelve el nodo a `number` — o sea que el
arreglo solo aguanta la PRIMERA edición de cada foco. Se gana esa carrera con `queueMicrotask`.
Probar SIEMPRE el gesto 2-3 veces seguidas sin desenfocar: uno solo pasa en verde con el bug puesto.

Ver [[campo-que-muestra-un-formato-y-guarda-otro-descarta-la-edicion-en-silencio]]
