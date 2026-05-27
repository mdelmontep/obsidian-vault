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
