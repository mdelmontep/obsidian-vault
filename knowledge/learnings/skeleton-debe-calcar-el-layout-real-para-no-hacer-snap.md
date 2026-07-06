---
title: el skeleton debe calcar el layout real (chrome + line-box) o hace "snap" y parece 2 cargas
date: 2026-07-06
source: claude-code-session
tags: [react, frontend, skeleton, ux, loading]
---
Gatear por `data.length===0` no basta (ver [[skeleton-de-loading-debe-gatear-por-data-length-no-solo-loading]]). Para que skeleton→contenido sea UNA carga sin brincos, el skeleton debe calcar el layout final:

- **Un SOLO skeleton de página completa** (chrome: tabs/búsqueda/filtros + grid), reusado en `loading.tsx` (Suspense) Y como early-return del componente cliente mientras `dataLoading && data.length===0`. Dos skeletons distintos = se percibe "2 cargas" + snap del toolbar al montar.
- **Nada de empty-state durante la carga**: mostrar "aún no tienes X" mientras el fetch corre da un flash "vacío→N items". Empty-state solo con `!loading && length===0`.
- **Alturas = line-box del texto real, no el glifo**: una barra de 11px + margin 1px queda apelotonada; el texto real ocupa font×line-height (nombre ~20px, meta ~16px). Slot con `min-height` del line-box + barra fina centrada.
- **El chrome debe ocupar las MISMAS filas** (p.ej. búsqueda con `flex:1 1 220/max320` para compartir fila con los filtros, no full-width que los empuja abajo).
- Verificar midiendo: el 1er item debe arrancar en el MISMO `y` en skeleton y en real (Playwright `getBoundingClientRect().top`). Caso TuFacturaIA: Y=353 en ambos → 0 salto.
- Reusar las clases reales (`.cc-*`) hereda spacing/divisores → altura de card = real.
