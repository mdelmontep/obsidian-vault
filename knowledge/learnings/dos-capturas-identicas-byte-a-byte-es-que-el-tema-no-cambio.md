---
title: dos capturas idénticas byte a byte es que el tema nunca cambió
date: 2026-08-26
source: facturaia
tags: [qa, playwright, dark-mode, arnes, facturaia]
---

QA de una tarjeta en claro y oscuro con Playwright: `emulateMedia({ colorScheme: 'dark' })`
y captura. Los dos PNG salieron con **el mismo tamaño exacto** (75.472 bytes). Ese es el
tell: el oscuro no se pintó nunca y la captura habría certificado un tema inexistente.

TuFacturaIA no lleva el tema por `prefers-color-scheme`: `useTheme()`
(`src/hooks/use-theme.ts`) lo escribe en `document.documentElement.dataset.theme` leyendo
`localStorage['af-theme']` (legacy `af-tema` = claro/oscuro/auto). Emular el media query no
toca nada.

- Sembrarlo con `page.addInitScript` **antes** del `goto`.
- **Verificarlo, no asumirlo**: leer `dataset.theme` y abortar si no es el pedido. Un arnés
  que no comprueba su precondición mide otra cosa y sale verde
  ([[arnes-con-asserts-de-eco-y-falso-verde-no-detecta-nada]]).
- Corolario barato: comparar el tamaño de las dos capturas. Iguales = no hubo tema.

`emulateMedia` solo sirve donde el CSS depende de verdad del media query.
