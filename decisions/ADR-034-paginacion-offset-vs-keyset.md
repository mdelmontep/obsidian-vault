---
title: "ADR-034: Paginación UI interna — offset vs keyset"
date: 2026-06-19
status: decided
tags: [facturaia, paginacion, bd, arquitectura]
---

## Contexto

TuFacturaIA no tenía paginación. Todas las listas (facturas, clientes, presupuestos, inventario) cargaban registros completos y filtraban en cliente. Con el crecimiento de orgs, PostgREST trunca silenciosamente a 1.000 filas.

## Alternativas consideradas

**A — Keyset/cursor:** `WHERE (created_at, id) < (:cursor)`. O(1) en BD. Sin salto a página N. Ya implementado en API v1 con HMAC firmado (`src/lib/api/v1/cursor.ts`).

**B — Offset server-side:** `.range(offset, offset+limit-1)` + `{ count: 'exact' }`. Permite salto a página N. Degradación O(n) a >50k filas.

## Decisión: Offset (B) para UI interna

- Ninguna org supera 5k registros a corto/medio plazo — la degradación de offset no aplica.
- Permite salto a página N (UX relevante para facturas numeradas).
- ~60% menos trabajo: los filtros client-side se migran limpios a `.eq/.gte/.lte` server-side.
- La API v1 pública mantiene keyset — dominios separados, sin contradicción.

## Consecuencias

- `PaginationBar` muestra pills numeradas (no solo Anterior/Siguiente).
- Los filtros de cada vista se mueven de `useMemo` client-side a parámetros de query Supabase.
- Estado en URL (`?page=1&limit=50`). Limit persiste en `localStorage`.
- Si el volumen por org supera 50k filas en el futuro, migrar a keyset sin cambiar la UI (keyset bajo el capó, UI de páginas numeradas con cursor-stack).
