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

## Modales y popovers

- **Popover dentro de modal con `overflow: hidden` se corta** — el ancestro clipa al popover absoluto. Soluciones: portal con `position: fixed` + `getBoundingClientRect`, o disclosure inline (el popover es un `<div>` siguiente que empuja contenido). Inline es más simple y mejor en móvil. Ver [[popover-en-modal-con-overflow-hidden-se-corta-usar-inline-disclosure]]

## Mobile Auth — Inputs y touch targets

- **iOS zoom = `font-size < 16px` en inputs** — Safari auto-hace zoom cuando el input enfocado tiene font-size < 16px. Fix definitivo: `font-size: 16px` en todos los `input`, `select`, `textarea` en la hoja global.
- **Touch targets: `min-height: 44px` + `min-width: 44px`** — aplica a botones, password-eye toggles y cualquier elemento interactivo pequeño.
- **Password-eye con padding en vez de size** — `padding: 12px` en el botón + `min-width/height: 44px`. Ajustar `padding-right` del input al nuevo tamaño del botón.
- **`env(safe-area-inset-*)` en pantallas auth mobile** — `padding-bottom: env(safe-area-inset-bottom, 16px)` en el scroll container. Sin esto el contenido queda cortado bajo el home bar de iOS.
- **`inputMode="tel"` en campos de teléfono** — abre teclado numérico en iOS/Android directamente, sin depender del `type="tel"`.

## CSS Grid · trampas de layout en cards móvil

- **2+ items con el mismo `grid-area` se solapan en la misma celda** — si tienes 2 `<td>` o `<div>` apuntando a `grid-area: footer`, el segundo se renderiza encima del primero, no debajo. Solución: usar `grid-column: 1 / -1` en cada uno y dejar que `grid-auto-flow: row` (default) los coloque en filas implícitas sucesivas. Caso real NotCaído mobile: `down-since` + `error chip` ambos con `grid-area: footer` → solapados invisibles. Fix: `grid-column: 1 / -1` en ambos.

- **Columna `auto` toma el ancho del item más ancho de CUALQUIER fila** — `grid-template-columns: auto 1fr auto` con un dot 14px (col 1 row 1) y un toggle 48px (col 1 row 3) hace que la col 1 mida 48px en TODAS las filas. Resultado: el dot de la fila 1 queda con un hueco enorme a su derecha. Solución: usar más columnas + `grid-template-areas` con span (`"dot name name" / "dot probes probes" / "tog tog acts"`) para que la col del dot no comparta tamaño con la col del toggle.

- **Cache-bust manual de CSS en Jinja/HTMX/Flask** — incrementar `?v=N` en `<link rel="stylesheet" href="/static/styles.css?v=N">` cada vez que cambias el CSS. Sin esto, deploys con caché agresivo (Cloudflare, Dokploy + Traefik con `Cache-Control: public, max-age=...`) no se ven en clientes que tengan la versión vieja. Caso real NotCaído: bumps `v=11→12→13→14` durante iteración móvil.
