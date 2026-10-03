---
title: stylelint declaration-strict-value no ve rgba() ni oklch(), ni siquiera en color
date: 2026-10-04
source: facturaia
tags: [css, stylelint, tokens, design-system]
---

`scale-unlimited/declaration-strict-value` con `["/color/","fill","stroke"]` parece «prohibir color crudo», pero:
- Solo mira esas propiedades: `background`, `border`, `box-shadow` con hex o `rgba()` pasan.
- `ignoreFunctions: true` es el default del plugin: `color: rgba(…)`, `oklch()`, `lab()`, `color(display-p3 …)` pasan incluso en `color`.

Fix/patrón: no citar la regla como candado único. Complementar con un trinquete por fichero que cuente hex y `rgb()/hsl()` en `.css` (en facturaia: `hex` y `colorFn` de `scripts/design-debt-ratchet.mjs`, PR #3226). Lo que sigue sin candado (`oklch`, nombres como `white` en `background`, `rgba` en `.tsx`) se declara en la doc de gobernanza, no se da por cubierto.
Verificar con un caso que DEBE fallar antes de afirmar que la regla lo para. Ver [[color-mix-in-srgb-para-sombras-tematizables]].
