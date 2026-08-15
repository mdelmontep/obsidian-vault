---
title: queryReplacement trocea por comas todo valor que no sea json
date: 2026-08-15
source: claude-code-session
tags: [n8n, postgres, expresiones, elphis, gotcha]
---
El nodo Postgres (>= 2.5) evalúa cada `{{ }}` de `queryReplacement` y luego, si el resultado
**no es JSON válido**, lo pasa por `stringToArray` — que parte por comas
(`Postgres/v2/actions/database/executeQuery.operation.ts`):

```js
const evaluatedValues = isJSON(expr) ? [expr] : stringToArray(expr);
```

Un `error_message` con una coma se convierte en dos parámetros y **desplaza todos los
siguientes**: `$5::jsonb` recibía el valor de `$4` → `invalid input syntax for type json`.
Con `onError: continueRegularOutput` el INSERT moría en silencio: **cualquier error con coma
en el mensaje llevaba meses sin registrarse**. Por eso el JSON del payload no rompía nada
(es JSON, pasa entero) y el texto de al lado sí.

Patrón: **un solo parámetro y que sea JSON**. `$1::jsonb` y desempaquetar en SQL con
`d->>'campo'`, `FROM (SELECT $1::jsonb AS d) p`. Inmune a comas, comillas y acentos.
(El `.replace(/,/g,';')` que aparece en algunos nodos es el parche de alguien que ya se lo
encontró.)
Ver [[una-expresion-que-evalua-a-null-viaja-como-el-texto-null]] · [[el-nodo-postgres-emite-success-true-cuando-el-returning-sale-vacio]]
