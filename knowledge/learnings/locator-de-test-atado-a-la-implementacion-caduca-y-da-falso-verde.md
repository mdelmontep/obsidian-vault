---
title: locator atado a la implementación caduca, y dentro de un if da falso verde
date: 2026-07-27
source: claude-code-session
tags: [e2e, playwright, testing, refactor, facturaia]
---

Cuando la UI mejora, los locators atados a su implementación se podrían solos. Seis casos en una
sola suite (TuFacturaIA, 2026-07-27): `title` nativo → componente `Tooltip`; `<select>` nativo →
`<Select>` compartido (×2); clase `.toast` → CSS Module (`toast-module__<hash>__toast`, y sin
`role`); columna renombrada; componente mudado del sidebar al topbar por viewport.

Un locator que resuelve a **0 elementos no es evidencia sobre el producto, es un test roto**:
- Da rojo que se aprende a ignorar. `.status-pill[title]` contaba 0 SIEMPRE y el test se llamaba
  "expone tooltip": llevaba meses sin verificar nada.
- O **falso verde** si vive dentro de un `if (await x.isVisible())`: el bloque nunca entra y el
  test pasa sin comprobar. Ese es el peligroso.

Reglas:
- Afirmar por **rol + nombre accesible**, o por el contrato que el componente publica
  (`aria-controls` del trigger, región `aria-live`), nunca por clase de CSS Module ni etiqueta nativa.
- Ojo con `.last()` sobre roles genéricos: `[role="listbox"]` también lo era la lista de la página,
  siempre visible, así que un `toBeHidden()` esperaba en vano.
- Al depurar, **mirar el aviso inmediatamente**: concluí que un error no avisaba al usuario porque
  miré los toasts 12 s después del clic; salía a los 750 ms y el producto estaba bien.

Ver [[e2e-smoke-skip-honesto]] · [[arnes-con-asserts-de-eco-y-falso-verde-no-detecta-nada]] · [[facturaia]]
