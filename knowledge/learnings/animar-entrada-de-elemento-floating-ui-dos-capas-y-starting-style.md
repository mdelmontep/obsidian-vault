---
title: animar la entrada de un tooltip/popover de floating-ui necesita 2 capas + @starting-style
date: 2026-07-06
source: claude-code-session
tags: [frontend, react, floating-ui, css, animation, starting-style]
---

Dos gotchas independientes al añadir una animación de entrada (scale/blur) a
un tooltip posicionado con `useFloating`, confirmados con Chrome DevTools
Protocol muestreando `getComputedStyle` frame a frame:

**1. No animar `transform` en el mismo nodo que posiciona floating-ui.**
`floatingStyles` escribe `transform: translate(x,y)` inline, recalculado en
cada frame por `autoUpdate`. Si el CSS del propio nodo también anima
`transform: scale(...)` para la entrada, ambos compiten por la misma
propiedad — el navegador interpola el salto de `(0,0)` a la posición real
como si el elemento "viajara" desde la esquina. Fix: dos nodos — un wrapper
exterior que floating-ui posiciona (sin transición CSS), y un nodo interior
con toda la animación sobre SU PROPIO `transform`, que floating-ui no toca.

**2. El estado `initial` de `useTransitionStatus` no llega a pintarse.**
Al ser la primera vez que el elemento existe en el DOM, floating-ui pasa de
`status='initial'` a `status='open'` en el mismo ciclo sin frame intermedio
real — el selector `[data-status='initial']` SÍ matchea (`el.matches()` lo
confirma) pero su computed style ya es el de `'open'` cuando se puede leer.
Sin frame previo pintado no hay nada de qué partir para interpolar. Fix:
`@starting-style` (mecanismo del spec CSS para animar la primera aparición
de un elemento) para la ENTRADA; `[data-status='close']` sigue funcionando
normal para la salida (esa sí viene de un frame `'open'` ya pintado).

Caso: TuFacturaIA `src/components/ui/tooltip.tsx`/`.module.css`. Ver
[[floating-ui-strategy-fixed-vs-absolute-desplaza-tooltip]].
