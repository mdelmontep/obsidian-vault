---
title: castear .data de una query supabase oculta el 42703 que el tipo ya detecta
date: 2026-07-16
source: claude-code-session
tags: [supabase, postgrest, typescript, type-safety, eslint]
---
postgrest-js YA tipa `data` como `SelectQueryError<"column X does not exist">` si un `.select` pide una columna inexistente → usar el campo da TS2339. Pero el código lo tapaba: `(data ?? []) as X[]`, `data as X`, `.maybeSingle<T>()` (genérico explícito) DESCARTAN ese error → el 42703 pasa a runtime en silencio (resultado vacío). Ver [[supabase-select-columna-inexistente-falla-query-entera-42703]] · [[column-list-drift-clientes-proveedores-select-inexistente-42703]].

Además: postgrest SOLO infiere/valida columnas desde un `.select` con STRING LITERAL (o `as const`, incl. template `` `${A} , b` `` de literales). Un select concatenado con `+` o construido en runtime desactiva la detección aunque no castees.

Fix (erradicado 100% en TuFacturaIA, 9 PRs, ~450 casts, guardarraíl global `src/**`): quitar el cast → dejar fluir la inferencia; select literal; narrow en el borde para enum/jsonb/nullable (`x ?? fallback`, guard `includes`), NUNCA `as` ciego. RPC (`.rpc()` → `Json`) no es 42703: narrow aparte (helper).

CAVEAT capa componentes: si el cliente NO lleva `<Database>` (p.ej. `useOrgClient()` en TuFacturaIA, tipado `SupabaseClient` a secas por el proxy de impersonación), postgrest NO valida columnas (schema `any`) → quitar el cast NO da protección 42703; peor, en **embeds** devuelve `GenericStringError`/to-many array que obliga a cast de borde. La protección real solo vuelve tipando el cliente `<Database>` (cascadea a todos los consumidores). El fix de "quitar cast" solo cierra el 42703 en clientes tipados.

Guardarraíl ESLint `no-restricted-syntax` scoped por carpeta (burndown como `forbid-dom-props`): marca `data`/`.data` casts, genérico en single/maybeSingle/returns, y `(… ?? []) as T[]` name-agnostic (caza el `data` renombrado). CLAVE: `?? []` (array-coalesce) = lista de query → marcar; `?? {}` = narrow jsonb legítimo → NO marcar. Esa distinción = 0 falsos positivos. El lint como VERIFY objetivo hace segura la paralelización con subagentes (no pueden recaer en el cast). Ver [[supabase-subagent-driven-development-paralelo-requiere-commits-y-archivos-exclusivos]].
