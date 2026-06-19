---
title: hook paginado + hook índice separado para views con búsqueda in-memory
date: 2026-06-19
source: claude-code-session
tags: [react, pagination, hooks, tufacturaia]
---

**Problema**: al paginar una view que tiene funcionalidades que necesitan la lista completa
(merge modal, detección de NIFs duplicados, URL focus `?id=X`), la página actual no tiene
todos los datos.

**Patrón**: dos hooks separados.
- Hook paginado (`useClientesData`): query con `.range()` + `{ count: 'exact' }` + stats por página.
- Hook índice (`useClientesIndex`): carga ligera de todos los registros (solo 3-4 columnas, sin stats).

**Mutations**: `reload()` incrementa `refreshKey` del paginado. `indexReload()` incrementa `indexRefreshKey` del índice. Ambos son `useCallback(() => setState(k => k+1), [])`.

**Autologo eliminado**: en el modelo paginado no tiene sentido iterar todos los items al cargar;
el logo se gestiona por menú contextual (subir/buscar).

**Test**: mockear dos tablas distintas en `mockFrom(table)` → chain de contactos (ends with `.range()`)
y chain de facturas (thenable directo via `then` getter).

Aplicado en: `use-clientes-data.ts` + `use-clientes-index.ts` (FacturaIA, issue 006).
