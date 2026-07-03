---
title: new Date(y,m,d).toISOString() desplaza la fecha un día fuera de UTC
date: 2026-07-03
source: claude-code-session
tags: [javascript, timezone, fechas, bugs-silenciosos]
---
`new Date(2026, 6, 1)` crea medianoche LOCAL (Madrid UTC+2) = `2026-06-30T22:00Z`;
`.toISOString().split('T')[0]` devuelve `'2026-06-30'` — un día ANTES. Cualquier
rango de fechas construido así queda corrido un día en ambos extremos.
Caso real FacturaIA /informes: el "trimestre actual" iba del 30-jun al 29-sep —
el widget IVA, la comparativa y los CSVs incluían facturas ya declaradas en el
trimestre anterior y perdían el último día del propio (PR #657).
Fix: construir rangos fiscales con aritmética de strings (`rangoIsoDelPeriodo`
en `src/lib/fiscal/periodo.ts`, client-safe) y el "hoy"/periodo actual con
Intl + timeZone explícita (`periodoDe`). Regla: NUNCA `toISOString()` para
obtener un YYYY-MM-DD de una fecha construida en local.
