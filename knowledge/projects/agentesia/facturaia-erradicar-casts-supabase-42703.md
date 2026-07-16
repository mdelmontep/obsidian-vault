---
title: FacturaIA — Erradicar la clase 42703 quitando los `as` casts sobre resultados de queries Supabase
date: 2026-07-15
source: claude-code-session
tags: [facturaia, supabase, typescript, type-safety, deuda-tecnica]
---

> **ESTADO: PARCIAL — burndown EN CURSO (2026-07-16).** Guardarraíl cubre **9 zonas** (~290 casts erradicados); quedan **~250 casts** en el resto del repo.
> - **Mergeado a prod** (4 PRs + smoke real supabase-js 0×42703): #926 fiscal+guardarraíl base · #931 conciliacion+documents+helper `rpc-result` · #933 admin+internal+integrations · #935 endurecer regla (casts con `data` renombrado) + 54 con alias. → 7 carpetas.
> - **En PR #944** (sin merge): `src/lib/copiloto/**` + `src/app/api/**` (~105 casts; tests copiloto 752 + api 936). Bug real: `voice/cashflow` `.select` de `cashflow_events` no traía `org_id/created_at/updated_at` que el mapper usa.
> - **PENDIENTE** (~250 casts, ~90 ficheros): resto de `src/lib/**`, `src/components/**` (los client components SÍ hacen queries directas → casts reales), `src/app/**` no-api + `src/hooks/**`. Se intentó full-repo con 5+3 agentes pero la infra cortó 4 (session-limit + connection-closed); trabajo parcial en stashes locales (a dropear en fresh session). **Prompt de continuación estructurado entregado al usuario** (patrón agente-por-zona gateado por lint, máx 2-3 concurrentes). Ver [[orquestar-subagentes-paralelos-burndown-grande-limites-y-checker]].
> - Learning núcleo: [[casts-sobre-data-de-query-supabase-ocultan-42703-que-el-tipo-ya-detecta]].

# Objetivo

Que un `.select('columna_inexistente')` (o filtro/order) sea **error de compilación de verdad**, para matar la clase entera de bug **42703** en runtime (PostgREST `column does not exist`). Caso que lo motivó: 5 bugs 42703 en una sesión (Holded `PROVEEDOR_COLS.updated_at` #918 + 4 más en #922: `presupuestos.iva_pct`, `lineas_factura.created_at`, `plan_features.plan_id`, `facturas.num_factura`), todos con resultado vacío en silencio.

# Diagnóstico (ya hecho, NO re-investigar)

El sistema de tipos YA detecta estos bugs, pero el código los oculta:
- Los clientes ya están tipados `<Database>` (`createClient<Database>`, `AnyClient = SupabaseClient<Database>`). NO es el problema.
- `src/lib/database.types.ts` está al día (verificado: `presupuestos` tiene `base/irpf_pct/total`, NO `iva_pct`).
- postgrest-js 2.103 tipa el select string: una columna inexistente hace que `data` sea `SelectQueryError<"column 'X' does not exist on 'T'.">`, y usar el campo da **TS2339** (probado con un fichero-sonda: sí falla el typecheck).
- **PERO** el código hace `(data ?? []) as DocRow[]`, `as unknown as PlanRow[]`, `(data as unknown[])?.[0]`… sobre el resultado → **el `as` descarta el `SelectQueryError`** y el typecheck pasa con el bug dentro.

Root cause: **casts (`as`) sobre `.data` de queries Supabase** que tiran la validación de columnas que el tipo ya trae gratis.

# Plan (fásico — hay muchos casts, no big-bang)

1. **Inventariar**: grep de `as .*\[\]` / `as unknown as` / `as \w+\)` cerca de `.select(`/`.from(`. Priorizar por superficie: rutas server + componentes user-facing primero; flujos poco ejercitados (integraciones off, admin, crons, módulos opt-in) son donde se esconden más 42703.
2. **Por cada cast, quitarlo y dejar fluir el tipo inferido**. Según qué salte:
   - Columna mal escrita/inexistente → bug real, arreglar (como los 5 de hoy).
   - Relación embebida que PostgREST devuelve como array (`clientes(nombre)` → `{nombre}[]`) → normalizar con el tipo inferido (`Array.isArray(x) ? x[0] : x`), no castear a ciegas.
   - Shape genuinamente distinto para el consumidor → mapear campo a campo (parse-don't-validate), NUNCA `as` global.
3. **Guardarraíl** para que no vuelva: lint rule custom o test que prohíba `as` sobre el `.data`/resultado de una query Supabase; o un helper tipado `rows<T>()` que valide en el borde. Sin esto, la deuda reaparece.

# Gotchas (de memoria del agente — respetar)

- NO tocar el `Database` global para tablas nuevas sin `gen:types` → rompe `AnyClient` en otros módulos. Usar cliente tipado local aislado (cast acotado). Ver memoria `reference_facturaia_extender_database_type`.
- `gen:types --linked` CUELGA desde la red del Mac (puertos Postgres bloqueados) → workaround `--project-id` + gotcha de caché. Ver memoria `reference_supabase_puertos_postgres_bloqueados_red`. Regenerar `database.types.ts` tras CADA migración para que no quede stale (un tipo stale reintroduce el fallo silencioso).
- Verificar un fix real por supabase-js contra prod (error=null), no por psql (psql no ve el 42703 de PostgREST).

# Aceptación

- Un `.select` con columna inexistente en cualquier flujo tocado → `npm run typecheck` FALLA.
- Idealmente un test/lint que lo garantice de forma general (impide el `as` que lo oculta).

# Coste / valor

Medio-alto (casts por todo el repo) → fásico, empezando por lo caliente + lo raramente-ejercitado. Valor: elimina en compilación una clase de bug que hoy solo se detecta en producción (o nunca, si el flujo no se ejercita). Ver learning [[column-list-drift-clientes-proveedores-select-inexistente-42703]] y regla `~/.claude/rules/type-safety-ts.md` (parse-don't-validate en bordes).
