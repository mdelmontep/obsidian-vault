---
title: guard que cace locators de E2E atados a una clase de CSS Module
date: 2026-08-09
tags: [inbox, facturaia, e2e, playwright, css-modules, hooks]
---

No construido. Idea que sale de una reincidencia medida, no de una intuición.

**El caso** (TuFacturaIA, 9-ago): el smoke `settings-auditoria.spec.ts` localizaba la
tabla con `table.set-table.audit`. Al día siguiente, el PR #1577 hasheó `.audit` a clase
de módulo y ese locator quedó **muerto**. Aquí un locator muerto no da rojo: da
`count() === 0`, que ese test interpreta como «no hay tabla». Lo cacé al correr el smoke,
no el arnés.

La regla que lo prohíbe ya existía y era **de 13 días antes**
([[locator-de-test-atado-a-la-implementacion-caduca-y-da-falso-verde]]), escrita por mí. Y
no estaba enterrada: `Stack/hot.md:80` la dice literal («nunca por clase de CSS Module») y
`hot.md` se carga en CADA arranque de sesión. Aun así no frenó nada. Es el patrón «regla
dura solo en prosa → hook» con la variante incómoda: **estar en el contexto no basta**.

**Forma candidata**: script en `pre-commit` que, para cada string de selector en
`tests/e2e/**`, extraiga los nombres de clase y falle si alguno está definido como clase
local en cualquier `src/**/*.module.css`. Barato (dos greps y un cruce) y determinista.

**Cabos a resolver antes de escribirlo**:
- Falsos positivos con clases que existen **a la vez** en `globals.css` y en algún módulo
  (`.set-table` no, pero habrá casos): el guard debe mirar si es local en el módulo QUE
  USA ese componente, o aceptar una lista blanca declarada en el propio spec.
- Los selectores llegan por template literal y por `getByRole(...)`; el guard solo debe
  mirar strings de `locator()` / `querySelector`, no cualquier literal.
- Verificarlo por el camino REAL (los casos que DEBEN bloquear son los que discriminan):
  el propio `table.set-table.audit` del #1576 tiene que hacerlo saltar.
