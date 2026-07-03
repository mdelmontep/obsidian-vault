---
title: extender el tipo Database de supabase-js sin romper el cliente tipado
date: 2026-07-04
source: claude-code-session
tags: [supabase, typescript]
---
Para tipar `admin.from('tabla_nueva')` antes de poder correr `gen:types` (rama en curso, mig sin desplegar), dos trampas:

1. **`Row`/`Insert` deben ser `type`, NO `interface`.** Una `interface` no satisface el `Record<string,unknown>` de `GenericTable` de supabase-js → TODO el cliente colapsa a `never` (síntoma: `Argument of type '{...}' is not assignable to parameter of type 'never'` en cada `.insert()`/`.update()` del proyecto entero).

2. **No extiendas el `Database` global** (ni `database-overrides.ts`). Varios helpers definen `type AnyClient = SupabaseClient<Database>` importando los tipos GENERADOS (sin tu tabla); si añades tablas al override, `SupabaseClient<OverridesDatabase>` deja de ser asignable a ese `AnyClient` → cascada de errores en ficheros ajenos.

**Fix:** cliente tipado LOCAL aislado en el módulo que usa la tabla — `admin as unknown as SupabaseClient<MiniDb>` con `MiniDb = { public: { Tables: { mi_tabla: {...} }, Views:{}, Functions:{}, Enums:{}, CompositeTypes:{} } }`. Se retira al correr `gen:types` post-deploy. Caso real: mig 428 `data_export_jobs` (FacturaIA). Ver [[gen-types-linked-no-db-url]].
