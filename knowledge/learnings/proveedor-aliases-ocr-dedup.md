---
title: "Aliases de proveedor: dedup OCR tras renombrar"
date: 2026-06-10
source: facturaia feat/fiscal-aeat (sesión 2026-06-10)
tags: [ocr, proveedores, postgres, trigger, aliases, dedup]
---

# Aliases de proveedor: evitar duplicados OCR tras renombrar

## Problema

OCR matchaba proveedor por `NIF OR nombre ILIKE`. Si el usuario corregía "Amazon" → "Amazon Spain SL", el siguiente scan no encontraba match y creaba un duplicado. Sin NIF (ticket de supermercado, gasolinera), el único anclaje era el nombre exacto.

## Solución

1. **Columna `aliases text[]`** en `proveedores` (mig 244).
2. **Trigger BEFORE UPDATE** `trg_proveedores_track_nombre`: cuando `NEW.nombre IS DISTINCT FROM OLD.nombre`, hace `NEW.aliases = ARRAY(SELECT DISTINCT val FROM unnest(NEW.aliases || ARRAY[OLD.nombre]) WHERE val <> '' AND val <> NEW.nombre)`. Usa `NEW.aliases` (no `OLD.aliases`) para respetar borrados manuales del usuario en la misma operación.
3. **Función SQL `resolve_proveedor(org_id, nif, nombre)`** SECURITY INVOKER: prioridad NIF exacto → nombre ilike → alias ilike. `FOUND` tras `RETURN QUERY LIMIT 1` funciona en PL/pgSQL (documentado: FOUND=true si RETURN QUERY devuelve ≥1 fila).
4. **OCR y pending-action** usan RPC `resolve_proveedor` en lugar del `.or()` PostgREST.
5. **UI**: modal edición muestra aliases como pills eliminables. Al guardar con rename, el estado React replica la lógica del trigger (`prevNombre !== nextNombre → añade prevNombre al array`).

## Gotchas

- El índice GIN array_ops NO acelera `lower(a) = ANY(SELECT lower(a) FROM unnest(aliases))`. Para volumen < 1000 proveedores/org el seq scan es aceptable. Si se necesita índice, normalizar aliases a lowercase al almacenar.
- `REVOKE EXECUTE FROM PUBLIC` en la función SQL para no exponerla vía PostgREST anon.
- Sincronizar estado React local con lo que hará el trigger en BD (evitar aliases stale hasta el reload).
