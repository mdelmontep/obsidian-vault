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

- **Peor que dentro de un `if`: detrás de un `test.skip(count === 0)`.** Eso no es un rojo que se
  ignora, es un **verde permanente**. Tres casos así en la misma suite (2026-07-28), y uno tapaba un
  bug de producto: el microtexto que el test decía cubrir llevaba **oculto por CSS**
  (`display:none`) desde un PR de junio. Markup que nadie veía y un test que decía verlo.
- **Y el simétrico: un locator que casa de MÁS.** `getByRole('img', {name: /^Gráfico de cashflow/})`
  casa también con `"Gráfico de cashflow vacío"`, así que el test pasaría con «Sin datos» pintado.
  Al escribir un locator, preguntarse con qué OTRA cosa casa, no solo si encuentra la buena.

Reglas:
- Afirmar por **rol + nombre accesible**, o por el contrato que el componente publica
  (`aria-controls` del trigger, región `aria-live`), nunca por clase de CSS Module ni etiqueta nativa.
- Ojo con `.last()` sobre roles genéricos: `[role="listbox"]` también lo era la lista de la página,
  siempre visible, así que un `toBeHidden()` esperaba en vano.
- Ante un spec que SALTA, comprobar que su locator existe hoy en el producto (grep del atributo, no
  del componente) antes de creerse el verde.
- **React 19 puede tener dos árboles montados** durante una transición: el locator resuelve a 2 y
  Playwright aborta por strict mode con la UI pintada y correcta. `:visible` o `.first()`, comentado.
- **Cuidado al retirar una aserción: puede estar haciendo de espera.** Al quitar la del chip del
  calendario destapé una carrera de hidratación que ella tapaba con sus 20 s: el clic caía sobre un
  botón sin manejador y el test moría dos pasos después, lejos de la causa.
- Al depurar, **mirar el aviso inmediatamente**: concluí que un error no avisaba al usuario porque
  miré los toasts 12 s después del clic; salía a los 750 ms y el producto estaba bien.

**Reincidió a los 13 días, y la escribí yo (9-ago, #1576→#1577)**: un smoke nuevo localizaba
`table.set-table.audit`, y al día siguiente el PR que hasheaba `.audit` dejó ese locator muerto —
`count() === 0`, que ese test lee como «no hay tabla», no como «test roto». La regla de arriba
(«nunca por clase de CSS Module») estaba escrita, era reciente y no frenó nada. **Al hashear una
clase, grep de su nombre en `tests/` EN EL MISMO PR**. **YA ES MECÁNICO** (#1578,
`scripts/locator-guard.mjs` en `pre-commit`): bloquea si un selector-string de `tests/e2e/**` usa
una clase que solo existe en `*.module.css`; con un `*.module.css` staged barre TODOS los specs,
porque el commit que mata el locator puede no tocar ninguno. Dos avisos del montaje: su primera
versión **salía verde sobre un repo con 2 hallazgos** (el contenido del string excluía toda comilla
y cortaba en `'[role="dialog"], .modal'`), y las clases que viven en global Y en módulo no bloquean
a propósito — un guard que adivina genera falsos positivos, y esos se desactivan.

Ver [[e2e-smoke-skip-honesto]] · [[arnes-con-asserts-de-eco-y-falso-verde-no-detecta-nada]] ·
[[empate-de-especificidad-entre-globals-y-un-module-lo-decide-el-orden-de-inyeccion]] · [[facturaia]]
