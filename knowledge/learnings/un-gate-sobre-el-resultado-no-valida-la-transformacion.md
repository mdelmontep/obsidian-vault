---
title: Un gate sobre el resultado no valida la transformación
date: 2026-08-07
source: TuFacturaIA · auditoría de la normalización de unidades del módulo Obras
tags: [learning, metodo, verificacion, gates, migraciones]
---

Al cambiar la unidad de un dato hay que reescalar dos campos a la vez: dividir
uno por un factor y multiplicar el otro. Puse como red de seguridad un gate que
comparaba el **resultado** (el precio de venta) antes y después, y abortaba la
migración si algo se movía.

**Ese gate no valida nada.** El producto `(x/f) × (y·f)` es invariante **por
construcción, para cualquier `f`**. Un auditor lo demostró simulándolo con
varios factores sobre los 11.595 materiales reales:

| factor | filas que hacen saltar el gate |
|---|---|
| 1,42 | 0 |
| 1,4918 (el que yo iba a usar) | 0 |
| 2 | 0 |
| **10** | **0** |

Con `f = 10` pasaba en verde. El gate comprobaba mi álgebra, no mi dato.

**La regla**: cuando el cambio es una transformación con un parámetro, el gate
tiene que atacar **el parámetro**, no el resultado. Si el resultado es invariante
por diseño, compararlo es una tautología cara.

El gate correcto aquí era sobre la **unidad**: el catálogo tenía 52 filas que
declaran en su propio nombre cuánto valen (`TIEMPO 0,5 HORAS`), así que después
de convertir se puede exigir que cada una valga lo que dice. Eso sí discrimina, y
además fue lo que destapó que **no había un solo factor sino dos** (1,42 y 1,49
conviviendo), lo que retiró la migración entera.

**Cómo detectarlo antes de escribirlo**: coge tu gate y pregúntate con qué valor
del parámetro fallaría. Si no encuentras ninguno, no es un gate. El mismo test
que aplicas a un hook (¿qué caso DEBE bloquear?) vale para un gate de datos: los
casos que deben pasar lo hacen trivialmente y no prueban nada.

Relacionado: [[dos-piezas-en-la-misma-unidad-equivocada-dan-el-resultado-correcto]] ·
[[la-confianza-autodeclarada-de-un-llm-no-predice-su-acierto]] ·
[[ejecucion-en-verde-no-prueba-el-efecto]]
