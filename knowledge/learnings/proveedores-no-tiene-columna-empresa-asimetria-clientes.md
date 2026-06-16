---
title: en facturaia `proveedores` no tiene `empresa` (sí `clientes`) → embed postgrest 500
date: 2026-06-16
source: claude-code-session
tags: [facturaia, supabase, postgrest]
---

Asimetría de schema fácil de pasar por alto: `clientes` tiene `nombre` **y** `empresa`
(razón social, persona jurídica); `proveedores` SOLO tiene `nombre` (NOT NULL), sin `empresa`.

Copiar el patrón de clientes a una query de proveedores rompe:
`.select('proveedores ( nombre, empresa )')` → 500 PostgREST
`column proveedores_1.empresa does not exist`. No salta en typecheck ni en tests con
mocks (el mock devuelve lo que le pongas) — solo en runtime contra BD real. Lo cazó Playwright.

Fix: en proveedores usar solo `nombre`. Nombre de display = `nombre` (sin fallback a empresa).
Regla general: al clonar una query entre dos tablas "gemelas", grepea las columnas reales
de la tabla destino antes de copiar el `.select()`. Ver [[playwright-domcontentloaded-no-espera-hidratacion-rsc]].
