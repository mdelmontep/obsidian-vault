---
title: objeto literal inline en deps de hook → render loop
date: 2026-06-21
source: claude-code-session
tags: [react, hooks, performance]
---

Pasar `{ a, b, c }` inline como argumento a un hook que hace:

```ts
const load = useCallback(async () => { ... }, [filters]) // filters = nuevo objeto cada render
useEffect(() => { void load() }, [load])                 // dispara siempre
```

…crea una referencia nueva en cada render → `load` cambia → effect dispara → `setLoading(true)` → re-render → bucle infinito.

**Fix (consumidor):**
```ts
const stableFilters = useMemo<T>(() => ({ a, b, c }), [a, b, c])
```

**Señal**: loading flickering continuo sin cambio de datos real.
Caso FacturaIA: `facturas-view.tsx` → `useFacturasData` (#439).
Ver también: [[proxy-impersonacion-reimplementa-api-supabase-se-desincroniza]] (mismo patrón, proxy en render).
