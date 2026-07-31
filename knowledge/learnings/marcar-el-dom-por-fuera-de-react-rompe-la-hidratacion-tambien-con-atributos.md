---
title: marcar el DOM por fuera de React rompe la hidratación, y con atributos también
date: 2026-07-31
source: claude-code-session
tags: [react, nextjs, hidratacion, hooks, css]
---
Un hook de "arrastrar para scrollear" hacía `el.classList.add(s.dragScroll)` sobre un contenedor
cuyo `className` lo pinta React. En la siguiente hidratación (navegación cliente-side, PPR) React
ve una clase que él no puso y avisa: *"some attributes of the server rendered HTML didn't match"*.

Dos trampas encadenadas:
1. **El aviso no lo explican los sospechosos de siempre.** Buscando por lectura de código salen
   `localStorage` en el `useState` inicial, `Date.now()` en render, `toLocaleDateString`. Ninguno
   era. Hay que reproducirlo en el navegador y leer el diff que imprime React, que nombra el nodo.
2. **Cambiarlo a `setAttribute('data-x','')` NO lo arregla**: React 19 diffea también los atributos
   que encuentra de más. Solo sobrevive el que se pone y se quita dentro de un gesto (`data-dragging`
   mientras el botón está pulsado), porque no llega vivo a una navegación.

Salida: que el hook no marque nada y el estilo cuelgue del selector con el que el hook ya busca los
contenedores (`.set-table-wrap { cursor: grab }`). De paso se ve que la marca no informaba de nada:
se añadía a todos los contenedores cableados, hubiera o no overflow.

Regla: si un efecto tiene que tocar `className` o un atributo persistente de un nodo que renderiza
React, el dato pertenece al render, no al efecto. Caso real: FacturaIA `/conciliacion`, `qa-015`.
