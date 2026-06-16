---
title: función postgres RETURNS composite con 0 filas → postgrest devuelve fila-de-nulls, no null
date: 2026-06-16
source: claude-code-session
tags: [postgres, supabase, postgrest, rpc]
---

Una función SQL `RETURNS <tabla>` que hace `UPDATE ... RETURNING * ` y no matchea
filas devuelve una "fila de nulls" (composite no-nulo con todos los campos NULL),
y PostgREST/supabase-js `.rpc()` la serializa como `{"id":null, ...}` — un objeto
**truthy**, NO `null`. Consumir con `data ?? null` lo deja pasar como objeto fantasma.

Caso real (runner Resolver-con-Claude): el RPC de claim con cola vacía devolvía
`{id:null,...}` → el runner lo tomaba por job válido → callback con `id=null` → app
400 en bucle apretado (9 req/s).

Fix en 3 capas: (1) guard app-side `const j = data; return j && j.id ? j : null`;
(2) reescribir el RPC en PL/pgSQL con `IF NOT FOUND THEN RETURN NULL` (PostgREST sigue
envolviendo el composite-null como fila-de-nulls, así que el guard es lo que cierra);
(3) el consumidor valida `id` antes de actuar. Lección: nunca confíes en que un RPC
composite devuelve `null` con 0 filas — valida un campo clave.
