---
title: CSS Module — kebab-case no convierte a camelCase (Next.js exportLocalsConvention 'asIs')
date: 2026-06-09
source: fix(admin) 9a55964 · reincidió #201/#202 2026-06-11
tags: [css-modules, nextjs, turbopack, gotcha]
---

Next.js usa `exportLocalsConvention: 'asIs'` por defecto (sin override en `next.config`): **no** convierte clases kebab→camelCase (no es webkit/Turbopack, es el default de css-loader en Next).

Si el CSS define `.kpi-grid` y el TSX accede `s.kpiGrid`, resuelve `undefined` → elemento sin estilos. Falla **silenciosa**: sin error en build/lint/typecheck, contenido visible pero sin layout.

**Patrón**: nombrar las clases del módulo en camelCase (`.kpiGrid`), o acceder por bracket `s['kpi-grid']`.

**Detectar**: por cada `s.camelCase` del TSX, comprobar que existe `.camelCase` (no `.kebab`) en su `.module.css`.

Casos reales: 4 paneles ia-ops sin layout (~30 clases/módulo); **2026-06-11 reincidió en 53 refs/12 ficheros** (modales presupuesto casi sin estilar, input `sr-only` visible) → #201/#202. En facturaia se fija en `docs/architecture/gotchas.md §Frontend`.
