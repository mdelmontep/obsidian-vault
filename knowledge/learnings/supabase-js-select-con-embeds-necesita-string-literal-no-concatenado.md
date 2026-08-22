---
title: supabase-js sólo infiere el tipo de un select() con embeds si es un string literal
date: 2026-08-04
source: claude-code-session
tags: [supabase, typescript, postgrest, tucrmia, facturaia]
---

`.from('webhook_deliveries').select('org_id, id, ' + 'webhook_endpoints(url, secret_encrypted)')`
compila pero el tipo de retorno es `GenericStringError` — todas las propiedades del embed dan
`TS2339: Property 'x' does not exist`. supabase-js parsea el STRING LITERAL del `select` en tiempo
de compilación (magia de tipos sobre el literal type) para inferir la forma con relaciones
anidadas; en cuanto el argumento es una expresión computada (concatenación con `+`, `.join()`,
variable), dejas de tener un literal type y el parser de tipos se rinde silenciosamente — sin
error de sintaxis, solo un tipo inútil.

Fix: escribe selects con embeds como un único string literal (o template literal sin
interpolación), nunca concatenado. Si necesitas construir el select dinámicamente, cástalo
explícitamente después con un tipo propio en vez de confiar en la inferencia.

Reincidió en TuFacturaIA el 22-ago (`change-plan-context.ts`, PR #2097) y venía TAPADO por un
`as unknown as` cuyo comentario culpaba a otra cosa —«`billing_accounts` aún no está en los tipos
generados»—, que llevaba meses siendo falso. Un cast con un porqué equivocado sobrevive a todas
las revisiones: nadie vuelve a comprobar el motivo que ya está escrito. Al quitarlo salieron los 8
`TS2339` de `GenericStringError` y con ellos la causa real.
