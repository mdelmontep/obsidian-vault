---
title: filtro de texto libre a columna tipada + error tragado = panel de ceros indistinguible de vacío real
date: 2026-07-13
source: claude-code-session
tags: [supabase, postgrest, ux, admin, observabilidad]
---

Un input de texto libre atado directo a una columna tipada (p.ej. `org_id uuid`)
sin validar deja meter basura ("pepe"). PostgREST responde 400 (coerción
`text→uuid`, 22P02), pero si el código hace `const { data } = await q` sin mirar
`error`, `data=null` → agregados a 0. En un panel de KPIs eso NO parece un fallo:
parece una entidad real sin actividad ($0.00, "0 decisiones", gate cerrado). El
operador cree estar viendo datos legítimos.

Dos fallos combinados, arreglar los dos:
- **Error tragado** → destructurar y propagar (`if (error) throw`). Ver
  [[supabase-js-catch-sobre-query-es-codigo-muerto]] · [[supabase-js-in-uuid-column-text-empty]].
- **Input libre a columna tipada** → sustituir por selector de valores válidos
  (combobox por nombre sobre un endpoint de listado), nunca pegar el id crudo.

Caso real: FacturaIA `/admin/ia-ops` (#850) — filtro `org_id` aceptaba cualquier
string y pintaba ceros. Regla general: en agregados, un cero puede ser un error
enmascarado; el estado "vacío" debe ser distinguible del "falló la query".
