---
title: una aserción E2E que mide DATOS en vez de montaje da verde o rojo por azar
date: 2026-08-09
source: claude-code-session
tags: [e2e, playwright, testing, facturaia]
---

Al escribir la red de seguridad de un split, tres aserciones parecían medir «el componente se montó» y en realidad medían «la org de test tiene datos». Los tres modos, todos vistos en la misma tanda:

1. **Tabla que solo se pinta si hay filas** (si no, `EmptyState`). El spec se caía con la vista sana. Fija `tabla O estado vacío`, nunca la tabla a secas.
2. **Lista que navega con `router.push` en un `onClick`, sin `<a href>`.** Buscar enlaces devuelve 0 **siempre**, ni habiendo mil filas → el `test.skip("no hay datos")` se dispara mintiendo. Peor que un rojo: un verde que afirma lo contrario de lo que pasa. Pincha la fila (`role="button"` + `aria-label`).
3. **Pestaña cuya etiqueta lleva un contador pegado** (`Total` + importe) → `{ name: 'Total', exact: true }` no la encuentra ni cuando está. Usa `/^Total/`.

Regla: la aserción debe apuntar a algo que exista **siempre que el componente se monte** — un `role`+`aria-label` del contenedor, no su contenido. Y todo `test.skip` por datos debe poder distinguirse de un locator roto: si el motivo del skip no se puede falsar, no es precondición, es un bug tuyo.

Comprobación barata: rompe a propósito el montaje de la pieza (quita su `aria-label`, que **compila igual**) y confirma que se pone rojo. Ver [[baseline-de-screenshot-capturado-de-la-pagina-equivocada-es-verde-para-siempre]] · [[asercion-de-ausencia-necesita-fixture-que-pueda-fallar]].
