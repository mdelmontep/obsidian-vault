---
title: cuenta los motores que calculan el mismo número antes de arreglar uno
date: 2026-08-19
source: claude-code-session facturaia
tags: [arquitectura, fuente-unica, sql, metodo, cobros]
---
El importe que se le reclama a un cliente lo calculaban **dos** motores: una función SQL para el
cron (`cobros_pending_for_org`) y un espejo TS para todo lo demás (`pendienteCobrable` +
`yaCobradoPorFactura`). El issue (#1856) describía el bug **solo en el lado TS**. Arreglar ese lado
habría dejado el cron reclamando de más, con el PR cerrado y la suite verde.

Y el enunciado también contaba de menos **dentro** de su lado: decía que faltaba sumar el ledger,
cuando faltaban **dos de tres patas** (ledger `factura_pagos` y `factura_resto_conciliacion`).

👉 Antes de aceptar el enunciado de un issue sobre un número: `grep` de **quién más calcula ese
mismo concepto** (no del síntoma — del concepto: «lo ya cobrado», «lo pendiente»), y **enumera las
partes** que debería sumar contra la fuente canónica. Un espejo TS y su función SQL no se
typechequean entre sí: divergen en silencio y el síntoma es un importe plausible.

Fix estructural, no dos parches: las dos mitades **delegan** en la función canónica. Para el lote,
un abanico SQL (`JOIN LATERAL fuente(f.id)`) en vez de reimplementar la suma por lotes — reutiliza,
no copia. Si te encuentras sumando de nuevo una de las patas «solo aquí», ese es el bug otra vez.

Ver [[converger-canal-divergente-sobre-fuente-unica]] ·
[[importe-fiscal-no-es-importe-a-cobrar-retenciones]] ·
[[un-control-negativo-que-no-discrimina-invalida-el-test-entero]].
