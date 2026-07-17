---
title: rpc con returns table explícito devuelve subconjunto tras add-column y el cast ts miente
date: 2026-07-17
source: claude-code-session
tags: [supabase, postgres, rpc, types]
---
Un RPC de búsqueda/fuzzy con `RETURNS TABLE (col1, col2, …)` EXPLÍCITO congela las columnas
que devuelve. Si una migración POSTERIOR añade columnas a la tabla base pero NO redefine el RPC,
este sigue devolviendo el subconjunto viejo — sin error. Si la app castea el resultado al tipo Row
completo (`as RowCompleto`), los campos nuevos llegan `undefined`/`null` y TS no se queja (el cast
miente). Si esa fila alimenta un formulario de edición, el PATCH reenvía esos campos a null →
**corrupción de datos silenciosa** (caso real obras: buscar material → editar → `precio_tarifa=null`,
`unidad_precio=1` → precio ×1000). Riesgo alto con tracks de migración en PARALELO (el RPC en una rama,
el add-column en otra) — nadie ve el desajuste.
Fix: al añadir columnas a una tabla, `grep -rl "RETURNS TABLE" supabase/migrations` de RPCs sobre ella
y redefinirlas (DROP+CREATE: cambiar columnas OUT no admite CREATE OR REPLACE). Mejor aún: que el RPC
devuelva `SETOF <tabla>` en vez de listar columnas, así hereda los add-column. Relacionado:
[[supabase-create-or-replace-view-falla-tras-add-column]], [[postgres-asumir-columna-existente-en-trigger-rewrite-verifica-information-schema]].
