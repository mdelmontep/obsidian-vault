---
title: scroll shadows técnica Komarov con variable CSS para dark mode
date: 2026-05-18
source: claude-code-session
tags: [css, dark-mode, scroll, ux]
---

`background-attachment: local` + 2 radial-gradients = fade hint que aparece SOLO cuando hay overflow real. Pero `rgba(0,0,0,X)` desaparece sobre fondo oscuro → bug invisible en dark.

Fix: variable `--scroll-shadow` con override en `:root[data-theme="dark"]` a `rgba(255,255,255,.18)`. La sombra cambia automáticamente con el tema.

`scrollbar-width: none` + `::-webkit-scrollbar { display: none }` oculta scrollbar (MDN advierte por affordance, pero las sombras compensan).

Añadir `scroll-padding-inline: 16px` para que el chip enfocado por teclado no quede pegado al borde.

`scroll-snap-type` NO recomendado para chips (M3): anchos variables generan saltos. Ver [[scroll-snap-no-recomendado-para-filter-chips]].

Fuente: https://css-tricks.com/scroll-shadows-with-javascript-free-css/
