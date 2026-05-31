---
title: useeffect que sincroniza estado→url pisa los query params si corre antes de hidratar
date: 2026-05-31
source: claude-code-session
tags: [react, nextjs, frontend]
---

Filtros bookmarkeables en URL (`?kind=otp&q=…`) con dos efectos:
1. hidratar estado **desde** la URL al montar
2. sincronizar estado→URL en cada cambio (`history.replaceState`)

Bug: el efecto (2) corre en el **primer render con estado vacío** y borra los
params de la URL **antes** de que (1) los lea → al refrescar o pegar la URL los
filtros se pierden (URL queda limpia, selects vacíos). Diferir (1) con
`Promise.resolve().then(...)` NO salva: (2) corre síncrono tras el primer render,
antes que el microtask.

Fix: flag `hydrated`. El efecto de sync hace `if (!hydrated) return`; se pone
`true` junto al `setFilters(readFromUrl())`. Bonus: gatear también el fetch de
datos con `hydrated` evita un primer fetch con filtros vacíos (doble fetch).

Caso: FacturaIA `email-logs-panel.tsx` 2026-05-31. Aplica a cualquier panel con
filtros en URL (p.ej. agency-portal). Ver [[react-19-strict-bloquea-setstate-en-useeffect]].
