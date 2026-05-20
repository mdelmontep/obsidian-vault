---
title: ADR-008 — Matriz canónica `user_can_write_in_org` en BD + espejo TS
date: 2026-05-20
status: accepted
tags: [adr, facturaia, rls, permisos]
---

## Contexto
Tras introducir multi-org real (mig 120), las policies RLS existentes solo validaban `org_id` sin rol. Cualquier miembro autenticado podía mutar facturas/clientes/etc via Supabase JS directo. Endpoints con `createAdminClient` bypaseaban RLS y no tenían check uniforme.

## Opciones consideradas
- **A** — Matriz solo TS en `withApiAuth({requireWrite})`. Cubre endpoints pero RLS sigue abierta para JS directo.
- **B** — Policies inline con `rol IN (...)` literal por tabla. Defense en BD pero matriz dispersa en N policies; cambios sin coherencia.
- **C** — Función SQL `user_can_write_in_org(org_id, resource)` STABLE SECURITY DEFINER como single source of truth + espejo TS `role-matrix.ts` consumido por hook UI y `withApiAuth.requireWrite`.

## Decisión
**C**, porque centraliza la matriz en BD (defense real) y permite a UI/endpoints reflejar el mismo set sin drift. Compromiso: modificar matriz exige tocar SQL + TS + test vitest. La fricción es deliberada — protege contra cambios silenciosos.

## Consecuencias
Migraciones 121, 123, 127 extienden la matriz con resources nuevos (`team`, `categoria`, `catalogo`, `module_config`). Policies de 14 tablas core la consultan. Cualquier endpoint nuevo con admin client debe declarar `requireWrite` (linter manual, no enforce). Ver [[matriz-permisos-rol-aware-bd-mas-espejo-ts]].
