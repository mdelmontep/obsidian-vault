---
title: refreshKey en useEffect para invalidar hook paginado post-mutación
date: 2026-06-19
source: claude-code-session
tags: [react, hooks, paginacion, tdd]
---

Cuando un hook paginado (`useCallback` + `useEffect`) necesita recargarse tras
una mutación (delete, update, create) sin resetear la página:

- Añadir `refreshKey = 0` como parámetro al hook
- Ponerlo en `useEffect` deps, NO en `useCallback` deps
- El linter `react-hooks/exhaustive-deps` lo marca como innecesario en useCallback
  porque no aparece en el cuerpo de la función. En useEffect sí es semántico.

En el componente: `const reload = () => setRefreshKey(k => k + 1)`
Tras mutar → llamar `reload()` en vez de `setData(prev => …)` optimista.

Anti-patrón: poner refreshKey en useCallback → warning eslint en cada hook nuevo.
Caso: `usePresupuestosData` (issue 005), mismo patrón en 006-008.
