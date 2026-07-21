---
title: next 16 — rsc server-fetch da "algo mejor"; instantáneo = cache components (y su coste real)
date: 2026-07-21
source: claude-code-session
tags: [nextjs, performance, rsc, cache-components]
---
Ladder de velocidad en Next 16 App Router (medido en FacturaIA):

- **RSC server-fetch** (mover el fetch de `useEffect` cliente a `page.tsx` server + `loading.tsx`): quita el waterfall bundle→montaje→fetch → mejora **MODESTA** ("algo mejor"), NO instantánea. Tras la 1ª visita el chunk ya está cacheado; lo que hace lento cambiar de pestaña es datos+render, no el bundle.
- **Navegación INSTANTÁNEA de verdad = Cache Components**: `cacheComponents:true` + `use cache` (resolver org FUERA y pasarlo como argumento + `cacheTag(\`x-${orgId}\`)` + `updateTag` en cada mutación) + `unstable_instant` por ruta (Suspense solo NO lo garantiza).
- **Coste de adoptar cacheComponents en una app que fetchea en CLIENTE** (spike): el build solo rompe por route-segment-config MECÁNICOS (`dynamic='force-dynamic'`, `runtime='nodejs'`, `force-static` → quitarlos); **CERO** errores "uncached data outside Suspense" (no hay datos server que tapar). El build es tractable.
- **El riesgo real NO es el build**: es `<Activity>` (flag GLOBAL) → el estado de UI (dropdowns/modales/formularios) ya NO se resetea al navegar → auditar app-wide (cerrar en cleanup / derivar de URL / resetear en submit) + QA visual obligatoria.
- **Code-split de un modal grande = marginal** (~3%/ruta) si comparte deps; el First Load JS lo domina el View monolítico + el React shared, no los modales.

Ver [[in-select-func-fuerza-seq-scan-usar-any-array-initplan]] · [[supabase-realtime-postgres-changes-filtrar-por-tenant-y-delete-replica-identity]].
