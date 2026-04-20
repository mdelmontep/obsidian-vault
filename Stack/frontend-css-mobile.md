---
title: frontend — CSS mobile y overflow
date: 2026-04-20
source: claude-md-migration
tags: [frontend, css, mobile, overflow]
---

# Frontend / CSS Mobile

## Overflow horizontal — causas y fixes

- **`flex` container tiene `min-width: max-content` por defecto** — un `div` o `p` con `display: flex` dentro de un CSS Grid sin `min-w-0` puede expandir el grid track y hacer la página más ancha que el viewport. Fix: `min-w-0` en el grid item + `min-w-0` en el flex container + `truncate` en los spans de texto largo.

- **`inline-flex` sin ancho explícito = riesgo de overflow en mobile** — un elemento con `inline-flex` que contiene texto largo se expande hasta su `max-content` y desborda. Siempre usar `flex w-full sm:w-auto sm:max-w-X` o al menos `max-w-full` cuando el contenedor es mobile.

- **`overflow-x: hidden` en ancestros no resuelve el overflow si no se elimina en el origen** — si un elemento es más ancho que el viewport, `mx-auto` centra dentro del layout width (más ancho), y el `overflow:hidden` recorta el lado derecho. La solución es añadir `min-w-0`/`overflow-hidden` en el elemento infractor, no en los ancestros.

- **`tracking-[N]` uppercase en flex container puede desbordar en pantallas < 375px** — textos con letter-spacing alto miden más de lo esperado. Siempre añadir `min-w-0` + `truncate` a spans dentro de flex containers con letter-spacing alto.

## Sticky headers y contenido en scenes móvil

- **Padding-top extra obligatorio cuando hay barra sticky flotante** — si una sección tiene una pill/nav sticky (ej: indicador de paso) que flota sobre el contenido, el primer scene necesita al menos 36-40px de padding-top en móvil. 18px no es suficiente y el título se solapa con la pill.
- **Números grandes + símbolo en móvil necesitan `whitespace-nowrap`** — "78%" se parte en "78" y "%" si el contenedor flex no tiene `whitespace-nowrap`. Aplica a cualquier stat card con número + sufijo (%, +, s, x).

## Checklist al depurar overflow en mobile

1. Buscar `inline-flex` sin `max-width` o `w-full` → cambiar a `flex` o añadir `max-w-full`
2. Buscar `flex items-center` sin `min-w-0` dentro de grid items → añadir `min-w-0` al grid item Y al flex container
3. Buscar texto con `tracking-[N]` o `uppercase` dentro de flex → añadir `truncate`
4. Añadir `overflow-x-hidden` a la sección que contiene el overflow, no solo al body/html
