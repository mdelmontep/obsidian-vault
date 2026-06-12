---
title: Un ancestro con backdrop-filter/transform anula el blur del popover descendiente → portar a body
date: 2026-06-12
source: claude-code-session
tags: [frontend, css, backdrop-filter, glassmorphism, portal, stacking, nextjs, facturaia]
---

Un popover con `backdrop-filter: blur(...)` que **cuelga de un ancestro que tiene `backdrop-filter` (o `transform`/`filter`/`will-change`)** sale **sin blur**, por mucho que subas la opacidad. Ese ancestro establece un *backdrop root*: el `backdrop-filter` del descendiente solo compone la imagen **dentro de la caja del ancestro**; las zonas del popover pintadas fuera de él (lo normal: un menú que se despliega por debajo) tienen backdrop vacío → `blur` efectivo = none.

Caso TuFacturaIA: los desplegables del topbar (empresa + avatar) colgaban de `<header class="topbar glass">` (`backdrop-filter` + `transform: translateZ(0)`). Se veían opacos/planos. Confirmado con **repro Playwright medida** (no a ojo): caja dentro de un header filtrado = rayas nítidas; misma caja a nivel `body` = esmerilada.

## Fix
Portar el popover a `createPortal(jsx, document.body)` (igual que el `Modal`), fuera del subárbol filtrado, con `position: fixed` calculada desde `getBoundingClientRect()` del trigger + guard `mounted` SSR. Click-outside debe comprobar también el `menuRef` (ya no está dentro del contenedor) y scroll/resize cierran (la posición queda flotando).

Distinto del otro gotcha de blur ([[frontend-css-mobile]]: `-webkit-backdrop-filter` a mano → lightningcss deja solo el `-webkit-`). Aquí el CSS compilado está bien; el problema es **dónde vive el nodo en el DOM**. Relacionado: [[modal-portal-stacking-sticky-sidebar]].
