---
title: typegen supabase modela NUMERIC como number; override de Database para bigint-as-string
date: 2026-07-02
source: claude-code-session
tags: [supabase, typescript, fiscal]
---
`supabase gen types` tipa NUMERIC como `number`, pero PostgREST acepta strings (y
Postgres los parsea con precisión exacta). Si persistes céntimos `bigint` serializados
a string (precisión fiscal), el cliente tipado rechaza el insert.
Fix canónico sin dependencias (patrón oficial Supabase, sin type-fest): fichero
`database-overrides.ts` que re-exporta `Database` con Omit+intersección sobre esa
tabla (`Insert: Omit<Gen['Insert'], K> & { col: number | string }`); los factories
de cliente importan Database del override, el resto sigue usando el generado.
NUNCA editar database.types.ts a mano (se regenera con gen:types).
Caso real: fiscal_declaracion_snapshot x100 en FacturaIA (PR #648).
