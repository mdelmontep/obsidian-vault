---
title: supabase-js no lanza en un insert fallido, así que el try/catch del caller es código muerto
date: 2026-08-01
source: claude-code-session facturaia
tags: [supabase, auditoria, seguridad, error-handling]
---
El patrón «audita ANTES de borrar y, si no puedes auditar, no borres» parecía cableado y no podía dispararse nunca. El helper de auditoría se tragaba **todo** fallo por dos vías independientes:

1. su propio `catch`, que convertía la excepción en un `console.error`;
2. supabase-js, que ante un error de insert **no lanza**: devuelve `{ data, error }` — y ese `error` no lo miraba nadie.

Resultado: el `try/catch` del caller destructivo era inalcanzable y el borrado seguía adelante igual, sin traza, que es justo el escenario para el que se escribió.

Regla: un helper «best-effort» (que loguea y sigue) **no** puede ser la base de un guard fail-closed. Si un caller necesita abortar, el helper debe tener un modo que relance de verdad — y comprobar el `{ error }`, no solo envolver en `try`. Test que lo fije: que exista el modo bloqueante, no solo que el caller lo pida.

Corolario: un test verde sobre el camino feliz nunca detecta esto, porque el fallo es una AUSENCIA. Candado estructural (leer el código y exigir la llamada) en vez de test de comportamiento.

Ver [[defensa-cableada-vs-codigo-muerto]] · [[helper-de-auditoria-con-early-return-deja-sin-traza-lo-global]]
