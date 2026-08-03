---
title: Un token de relleno no sirve como token de texto (marca personalizable a medias)
date: 2026-08-03
source: FacturaIA — color de marca por organización
tags: [design-tokens, accesibilidad, contraste, white-label]
---

Si el cliente elige su color de marca, hay que derivar **más de una** variable: el color que
rellena un botón casi nunca contrasta como texto (el azul de FacturaIA, 3,93:1 sobre blanco,
falla AA en cuerpo). De ahí que el sistema tenga `--brand` para rellenar y
`--brand-fg`/`--brand-fg-strong` para escribir.

El fallo: la pantalla de personalización pisaba solo `--brand` y `--brand-soft`. Con marca cyan →
botón cyan y, a 500 px, el ítem activo del menú azul. Dos marcas en la misma pantalla, visible en
cualquier captura, sin reportar en meses.

Derivar sin perder el contraste medido: buscar la variante más cercana al original que alcance el
ratio objetivo, no aplicar un `color-mix` fijo. En claro, multiplicar los tres canales por el
mismo factor conserva tono y saturación HSL exactos; en oscuro toca mezclar hacia blanco.
Calibrar los umbrales con los valores de fábrica para que el color por defecto no se mueva.

No romper a quien no personaliza: escribir en una variable de entrada que el token lee con el
valor de fábrica como fallback — `--brand-fg: var(--brand-fg-user-light, #2D6BE5)`. Y dos, una
por tema: un `style` inline en `:root` no tiene variantes de tema, y el derivado se oscurece en
claro pero se aclara en oscuro.

Comprobación en cualquier white-label: pon el naranja y busca texto azul.

Ver [[localstorage-global-en-app-multitenant-filtra-entre-organizaciones]].
