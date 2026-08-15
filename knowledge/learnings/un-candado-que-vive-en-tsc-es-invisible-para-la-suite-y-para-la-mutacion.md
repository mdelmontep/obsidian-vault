---
title: un candado que vive en tsc es invisible para la suite y para la mutación
date: 2026-08-15
source: claude-code-session
tags: [typescript, testing, mutacion, guards, tooling]
---

«Lo retiré del tipo, ya está protegido» es falso: el **excess-property check de TypeScript solo mira literales de objeto**. Medido — `f({ …, fila: 7 })` da `TS2353`, pero `f({ …, ...(c ? {} : { fila }) })`, `f({ ...ancha })` y pasar una variable ancha **pasan**. El tipo protegía **1 de 5** puertas.

Peor: al **borrar** el candado nuevo, `npm run typecheck` daba `ec=2` y la suite seguía en **179/179 verde**. Un barrido de mutación tampoco lo ve — corre sobre vitest, que transpila con esbuild y **no typechequea**. Así que las dos vías de verificación del repo dan verde con el hueco abierto.

**Patrón:** empujar el rechazo a la **asignabilidad**, que es lo único que atraviesa un spread: `T & { [K in Exclude<keyof T, keyof Contrato>]: never }` en la firma. Es invariante y no lista — lo prohibido sale de `keyof`, así que un campo legítimo nuevo se permite solo.

**Método:** si el candado vive en `tsc`, dilo y **mídelo con `tsc`**; presentar un «0 SIN VÍCTIMA» del barrido ahí es enseñar cobertura que no existe. Y descarta los flags globales con la cifra: `exactOptionalPropertyTypes` cerraba **0 de 5** y encendía 219 errores.

Ver [[un-guard-que-detecta-por-contenido-caza-los-comentarios-que-lo-niegan]] · [[mide-cuantos-pueden-fallar-antes-de-elegir-entre-n-candados-y-un-tripwire]]
