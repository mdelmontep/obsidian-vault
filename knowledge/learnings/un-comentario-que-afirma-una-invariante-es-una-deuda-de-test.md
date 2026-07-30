---
title: una afirmación en un comentario no es un guard — y explica por qué el bug sobrevivió a las revisiones
date: 2026-07-30
source: claude-code-session facturaia
tags: [auditoria, revision-codigo, metodo, tests]
---
Un comentario que dice que un riesgo está cubierto hace que el revisor deje de
comprobarlo. Es la razón por la que estos bugs sobreviven varias revisiones: quien
leyó el código encontró una frase tranquilizadora y no verificó la frase.

3 casos en la misma auditoría (TuFacturaIA, 400 controles):
- `number-field.tsx` — comentario decía que el campo parseaba formato ES. No lo
  hacía: `1.234,56` se guardaba como `1,23`. Llegó a una factura firmada. **P0**, y
  yo mismo estuve a punto de descartarlo por creerme el comentario.
- `more-menu.tsx` — "mismo criterio de ocultación que el Sidebar" mientras filtraba
  solo `oculto`, no `proximamente` → ofrecía módulos que redirigen.
- `anomaly.ts` — docstring decía que `posible_duplicado` "fuerza revisión humana".
  Ningún endpoint lo comprobaba.

**Corolario operativo: un comentario que afirma una invariante es una deuda de
test.** Si la frase merece estar escrita, merece un test que la sostenga; si no hay
test, debería decir "no comprobado" en vez de afirmar.

Al revisar: grepea la afirmación contra el código que la implementa, no contra su
vecindad. Bonus: el patrón reaparece DENTRO de los fixes (uno apagaba el contador
de módulos `beta` mientras su comentario decía "próximamente o bloqueado").
Ver [[defensa-cableada-vs-codigo-muerto]] · [[test-verde-puede-codificar-el-bug-como-esperado]].
