---
title: next.js — loading.tsx envuelve TODA la página en Suspense; router.replace de un query param ephemeral remonta tabs/toolbar, no solo la lista
date: 2026-07-21
source: claude-code-session
tags: [nextjs, app-router, suspense, performance, ux]
---
`loading.tsx` (o un `<Suspense>` inline en `page.tsx`) envuelve TODO el segmento de ruta, no solo el área "que carga". Si un componente hijo hace `router.replace()`/`router.push()` para reflejar en la URL un estado efímero de UI (página/límite/reset al cambiar de tab), esa navegación reabre el Suspense del segmento → discard-then-swap del árbol completo → el componente cliente se remonta desde cero (pierde `data`/estado) → su propio guard `loading && data.length===0` vuelve a disparar el MISMO skeleton. Resultado visible: "snap" a skeleton de página entera (tabs+toolbar+tabla) al cambiar de pestaña, no solo la lista actualizándose.

**Fix**: si el query param es solo cosmético/bookmarkable (no necesita re-render server), sacarlo del router — estado React local + `window.history.replaceState(null, '', url)` nativo. Cero navegación App Router = cero retrigger de Suspense/`loading.tsx`.

**Diagnóstico rápido**: ¿la ruta tiene `loading.tsx` (o Suspense inline) Y algún componente hace `router.replace/push` en la MISMA página al cambiar de tab/filtro? Si sí a ambas → candidato. Si el `router.push` navega a OTRA ruta, no aplica (esa sí debe mostrar loading).

Caso real: `usePaginationParams` (TuFacturaIA) — PR #1134. Ver [[skeleton-debe-calcar-el-layout-real-para-no-hacer-snap]] (bug relacionado pero distinto: ese es de layout visual, este es de remount real).
