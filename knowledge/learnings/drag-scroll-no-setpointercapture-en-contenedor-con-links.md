---
title: grab-to-scroll con setPointerCapture rompe los clicks de los hijos (links/botones)
date: 2026-07-20
source: claude-code-session
tags: [frontend, pointer-events, drag-scroll, react, gotcha]
---
Al implementar "arrastrar para scrollear" (grab-and-pan con ratón) sobre un
contenedor con overflow-x, la trampa es `el.setPointerCapture(pointerId)` en el
`pointerdown`: captura el puntero al contenedor y el `click` posterior deja de
llegar al `<a>`/`<button>` hijo → los clicks/navegación mueren (y arrastrar
sobre un link lo abre). Pasó en TuFacturaIA con las tabs de Obras (#1091→#1096).

Patrón correcto:
1. NADA de `setPointerCapture`. Los listeners de `pointermove`/`pointerup` van en
   `window` (el drag sigue aunque el puntero salga del contenedor, sin el efecto
   de captura sobre el click).
2. Engancha SOLO si hay overflow real (`scrollWidth - clientWidth > 1`); si no,
   no secuestres el puntero (tabs que caben deben dejar pasar el click).
3. Umbral (~6px) antes de considerar "drag": por debajo, click normal intacto.
4. Tras un drag real, tragar UNA vez el `click` sintético (capture, once) para
   no navegar al soltar sobre un link.
5. Suprimir el DnD nativo del `<a>`/imagen: `dragstart` → `preventDefault`.

Test de regresión clave: contenedor SIN overflow no marca dragging ni traga el
click. Ver [[postgrest-max-rows-trunca-silencioso-in-revienta-url]] (misma sesión).