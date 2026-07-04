---
title: columna nueva de una migración sin desplegar rompe el typecheck del .select() supabase
date: 2026-07-04
source: claude-code-session
tags: [supabase, typescript, migraciones, gen-types]
---
Distinto de [[supabase-select-columna-inexistente-falla-query-entera-42703]] (esa es runtime, columna que NO existe en BD). Aquí la columna SÍ existe en BD pero la migración aún no se ha aplicado a prod, así que `gen:types` (que lee el linked/prod) NO la incluye. El cliente tipado valida el string del `.select('...col_nueva...')` en compile-time y devuelve un tipo error-branded ("column 'x' does not exist on 'tabla'") → typecheck rojo en toda la query, incluso en campos que sí existen (billing_account, etc.).

Chicken-egg: no puedes regenerar tipos hasta desplegar la migración, pero el PR debe pasar typecheck antes.

Fix: castea SOLO el builder a un shape de lectura local (no toques el `Database` global — ver [[extender-database-supabase-interface-never-anyclient]]):
`const q = admin.from('t') as unknown as { select(q:string):{ eq(...):{ single():Promise<{data: RowLocal|null}>} } }`
Tras `db push` a prod → `gen:types` → retira el cast (la columna ya está en los tipos). Documenta el cast con "retirar tras gen:types".
