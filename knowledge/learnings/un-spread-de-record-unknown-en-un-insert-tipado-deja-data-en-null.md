---
title: un spread de Record<string,unknown> en un insert tipado deja data en null y el `as` miente
date: 2026-09-11
source: facturaia
tags: [typescript, supabase, testing, tipos, gotcha]
---
Un helper de test que compone la fila con `...campos: Record<string, unknown>` **rompe la
inferencia del cliente tipado de supabase-js**: el tipo de la fila deja de resolverse y
`data` acaba siendo `null`. El `as { id: string }` de encima no es un estrechamiento, es
una **conversión DESDE `null`**, y `tsc` la rechaza con `TS2352`.

El modo de fallo es peor que el error: de haber compilado, ese `as` habría tapado **justo
la fila que no llega**. No afirma «es un id», afirma «no es null» — lo único que quedaba
por comprobar.

Y no lo ve la suite: **vitest transpila con esbuild y no typechequea**, así que los tres
casos pasaban en verde. El único que lo vio fue el `tsc` del `pre-commit`, a 6 minutos de
gate en vez de a 20 segundos de test.

**Cura:** pasar el tipo al helper (`unwrap<{ id: string }>(...)`) en vez de castear el
resultado; cero `as` a tipo de dominio. El tell para buscarlos es `grep -rn "as [A-Z]"`,
no `grep any`. Ver [[un-candado-que-vive-en-tsc-es-invisible-para-la-suite-y-para-la-mutacion]]
