---
title: mockear una función compartida en el test de su consumidor oculta bugs de composición
date: 2026-05-27
source: claude-code-session
tags: [testing, vitest, correctness]
---
Cuando un endpoint COMPONE una función compartida (la llama con ciertos args) y el test mockea esa función, el test valida la lógica del endpoint PERO NO cómo la usa: pasar el argumento equivocado pasa verde (falso verde), porque el mock devuelve valores coherentes con el resultado esperado, no con el input real.

El bug solo aparece con la función real + datos no triviales — justo lo que el mock evita.

Fix: (a) test de integración sin mockear la función, o (b) aserción explícita sobre los args con que se llamó: `expect(mock).toHaveBeenCalledWith(..., expect.not.objectContaining({ clave_problematica }))`.

Caso FacturaIA: el doble conteo de `saldoInicial` pasaba verde porque el test mockeaba `buildCashflowData`. La regresión añadió `not.toHaveProperty('saldoInicial')`. Ver [[cashflow-saldo-actual-mas-serie-historica-doble-conteo]] · [[mock-supabase-fail-fast-default-en-tests-vitest]].

**Variante (2026-07-28): el fake cuya FORMA de retorno satisface la aserción.** No va de args, va del dato: el doble devuelve justo la forma que la aserción exige, así que el test verifica **la forma del fake**, no una propiedad del código.

- Caso: `expect(text).not.toContain("cuerpo largo")` con un executor fake cuyo `summarize` es multilínea **por invención del test**. En el código real, multilínea era 1 de 25 implementaciones: para las otras 24 la primera línea era el texto entero y el rótulo volcaba cuerpo de nota y PII. Verde, y la propiedad no existía.
- Los executors reales ya estaban cableados en ese mismo fichero de test.
- Segundo olor del mismo día: **`toMatchObject`/`objectContaining` para afirmar la AUSENCIA de una clave**. Empareja parcialmente → si mañana el objeto trae la clave prohibida, sigue verde. Para ausencia, `toEqual`.

Al revisar: *"¿esta aserción podría fallar alguna vez con la implementación real?"*. Si el fake ya cumple la premisa por construcción, recorrer las implementaciones reales y buscar la que la incumple. Caso agh-iberica PR #628/#629 → [[agh-iberica]]. Ver [[verificar-que-un-test-tiene-dientes-con-una-mutacion]] · [[arnes-con-asserts-de-eco-y-falso-verde-no-detecta-nada]].
