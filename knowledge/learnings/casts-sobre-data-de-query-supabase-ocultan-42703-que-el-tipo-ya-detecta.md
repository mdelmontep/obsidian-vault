---
title: castear .data de una query supabase oculta el 42703 que el tipo ya detecta
date: 2026-07-16
source: claude-code-session
tags: [supabase, postgrest, typescript, type-safety, eslint]
---
postgrest-js YA tipa `data` como `SelectQueryError<"column X does not exist">` si un `.select` pide una columna inexistente → usar el campo da TS2339. Pero el código lo tapaba: `(data ?? []) as X[]`, `data as X`, `.maybeSingle<T>()` (genérico explícito) DESCARTAN ese error → el 42703 pasa a runtime en silencio (resultado vacío). Ver [[supabase-select-columna-inexistente-falla-query-entera-42703]] · [[column-list-drift-clientes-proveedores-select-inexistente-42703]].

Además: postgrest SOLO infiere/valida columnas desde un `.select` con STRING LITERAL (o `as const`, incl. template `` `${A} , b` `` de literales). Un select concatenado con `+` o construido en runtime desactiva la detección aunque no castees.

Fix (erradicado en TuFacturaIA, 4 PRs, ~185 casts): quitar el cast → dejar fluir la inferencia; select literal; narrow en el borde para enum/jsonb/nullable (`x ?? fallback`, guard `includes`), NUNCA `as` ciego. RPC (`.rpc()` → `Json`) no es 42703: narrow aparte (helper).

Guardarraíl ESLint `no-restricted-syntax` scoped por carpeta (burndown como `forbid-dom-props`): marca `data`/`.data` casts, genérico en single/maybeSingle/returns, y `(… ?? []) as T[]` name-agnostic (caza el `data` renombrado). CLAVE: `?? []` (array-coalesce) = lista de query → marcar; `?? {}` = narrow jsonb legítimo → NO marcar. Esa distinción = 0 falsos positivos. El lint como VERIFY objetivo hace segura la paralelización con subagentes (no pueden recaer en el cast). Ver [[supabase-subagent-driven-development-paralelo-requiere-commits-y-archivos-exclusivos]].
