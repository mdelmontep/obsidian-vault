---
title: migrar a next 16 cache components — gotchas por etapas
date: 2026-07-22
source: claude-code-session
tags: [nextjs, next16, cache-components, performance, migration]
---
Activar `cacheComponents:true` (dynamic-by-default + PPR + `<Activity>`). Orden y trampas reales (FacturaIA, PR #1140):

- **Configs**: `runtime='nodejs'` es **INCOMPATIBLE** (build error, quitar); `force-dynamic`/`revalidate`/`fetchCache` obsoletos (quitar).
- **Route handlers GET** (el gotcha no-obvio): el `try/catch` del wrapper de auth **TRAGA** el throw de aborto de prerender de `headers()`/`connection()` → `HANGING_PROMISE_REJECTION`. Fix: `await connection()` como PRIMERA sentencia, **antes del try**. Un solo choke point (el wrapper) arregla decenas de rutas.
- **Páginas**: dato uncached al top-level fuera de `<Suspense>` rompe el build. Un `loading.tsx` en el segmento YA crea el `<Suspense>` que cubre el fetch propio de la página → añadirlo es el fix menos invasivo.
- **Layouts** (no los cubre loading.tsx): partir en cascarón estático + hijo async en `<Suspense>`; los `redirect()` funcionan dentro de Suspense.
- `new Date()`/`Math.random()` en server component antes de leer dato-request → error; `await connection()` primero.
- **Build env**: worktree fresco sin `.env.local` (gitignored) → el prerender construye clientes y peta `supabaseUrl is required`. Copiar el env al worktree.
- **`<Activity>`**: el estado UI NO resetea al navegar → overlays portaleados a body quedan flotando visibles; cerrarlos en cleanup de `useLayoutEffect` (hook `useCloseOnRouteHide`). QA visual obligatoria.
- Hasta cachear los datos (`use cache` per-org + `updateTag` en cada mutación) NO es más rápido en datos, solo en navegación (Activity/PPR).

Ver [[next16-rsc-algo-mejor-navegacion-instantanea-cache-components-coste]] · [[nextjs-rsc-seed-inicial-guard-contra-estado-solo-cliente]].
