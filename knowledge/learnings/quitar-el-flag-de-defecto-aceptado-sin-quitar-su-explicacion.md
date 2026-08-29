---
title: quitar el flag de un defecto aceptado sin quitar su explicación deja la mentira donde se mira primero
date: 2026-08-29
source: claude-code-session facturaia
tags: [documentacion, evals, metodo, revision-codigo]
---
Un defecto aceptado a sabiendas se marca **dos veces**: el flag que lo tolera y la prosa que explica
por qué. Viven en ficheros distintos, y el fix solo quita el flag — es el único que hace fallar algo.

Medido (facturaia #2279 → #2280). El caso `proforma-no-es-factura` era `knownBaselineGap` en
`__evals__/golden-set.ts`; el porqué estaba en `scripts/ocr-eval-fixtures/casos/…ts` («POR QUÉ HOY ES
`knownBaselineGap`», «NO se ha tocado el prompt en este PR»). El #2279 arregló el prompt y quitó el
flag; la prosa sobrevivió un día afirmando lo contrario.

- El daño no es un comentario viejo: **reencuadra una regresión futura como preexistente**. Quien vea
  el caso en rojo lee «esto ya fallaba» y cierra la investigación.
- El PR que cierra un gap **retira su explicación en el mismo commit**: qué rompía, qué lo arregló, y
  «un rojo aquí ya es una regresión».
- Al MARCAR un gap, cita el flag por su nombre en la prosa: así un grep del flag encuentra las dos
  mitades el día que alguien lo borre.

Ver [[un-comentario-no-puede-afirmar-el-estado-de-un-panel-de-deploy]] ·
[[un-comentario-que-afirma-una-invariante-es-una-deuda-de-test]]
