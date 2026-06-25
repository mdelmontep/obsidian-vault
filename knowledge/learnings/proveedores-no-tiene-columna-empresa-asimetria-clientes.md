---
title: clonar un `.select()`/forma entre tablas gemelas → grepea las columnas reales (el tipo TS puede mentir)
date: 2026-06-25
source: claude-code-session
tags: [facturaia, supabase, postgrest]
---

Al copiar una query o un payload entre dos tablas "gemelas", grepea las columnas reales
de la tabla destino antes: el tipo TS puede declarar un campo que la columna no tiene.
No salta en typecheck ni en tests con mocks (el mock devuelve lo que le pongas) — solo
en runtime contra BD real (`column X does not exist`, 400 `PGRST204` / 500). Lo caza Playwright.

Caso facturaia: `clientes` tenía `nombre` **y** `empresa` (razón social) desde mig 037;
`proveedores` solo `nombre`. El tipo TS `Proveedor` y el form compartido de `/clientes`
SÍ escribían `empresa` → guardar un proveedor con razón social/contacto: 400, no persistía.
Resuelto de raíz el **2026-06-25 (mig 387)**: `proveedores` ya tiene `empresa`, la asimetría
desapareció (quedó obsoleto el comentario de `informes/gastos/route.ts` que evitaba seleccionarla).
Ver [[campo-huerfano-shape-sin-migracion-paralela]] · [[consumidor-lee-claves-que-productor-no-emite]].
