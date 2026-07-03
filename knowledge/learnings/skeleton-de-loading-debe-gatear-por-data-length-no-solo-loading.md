---
title: skeleton de loading debe gatear por data.length===0, no solo por el flag loading
date: 2026-07-03
source: claude-code-session
tags: [react, frontend, pagination, ux]
---

Patrón anti: `{loading ? <Skeleton/> : <Tabla/>}`. Cada cambio de página/filtro pone `loading=true` un instante, y el skeleton (con un nº de filas o altura fija, normalmente menor que la tabla real) reemplaza TODA la tabla — la UI se encoge y luego vuelve a crecer de golpe al llegar los datos nuevos. Se nota mucho si el usuario pagina rápido.

Fix: el skeleton solo debe verse en la carga inicial (sin datos aún). Cambios posteriores con datos ya en pantalla se muestran atenuados (`opacity` + `pointer-events:none`) en vez de reemplazados:

```
const isInitialLoad = loading && data.length === 0
const isRefetching = loading && data.length > 0
```

Caso real: TuFacturaIA — mismo bug encontrado independientemente en 3 vistas (Auditoría, Conciliación, Inventario) porque cada una reimplementaba su propio loading state en vez de reusar un hook común. Al auditar una, merece la pena grepear `PaginationBar` en el resto del repo.
