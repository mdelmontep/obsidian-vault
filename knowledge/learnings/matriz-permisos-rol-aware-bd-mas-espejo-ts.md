---
name: matriz-permisos-rol-aware-bd-mas-espejo-ts
description: Patrón canónico SaaS B2B multi-tenant — matriz user_can_write_in_org(org_id, resource) SQL como single source of truth + espejo TS para UI/endpoints con service_role. Defense-in-depth.
date: 2026-05-20
source: claude-code-session
tags: [postgres, rls, supabase, permisos]
---

**Problema**: tener policies RLS per-tabla con `org_id = get_user_org_id()` sin discriminar rol → cualquier miembro autenticado puede mutar todo via Supabase JS directo. Tener role check solo en endpoints TS → cualquier endpoint que use `createAdminClient` (service_role) bypasea RLS y necesita check independiente.

**Patrón**: función SQL `user_can_write_in_org(p_org_id UUID, p_resource TEXT) STABLE SECURITY DEFINER SET search_path = public`. CASE hardcoded matriz rol×resource. Policies RLS UPDATE/INSERT/DELETE de cada tabla la consultan: `WITH CHECK (org_id = get_user_org_id() AND user_can_write_in_org(org_id, 'factura'))`. Espejo TS en `src/lib/auth/role-matrix.ts` (server+client neutral, sin 'use client'/'server-only') consumido por hook UI (`useOrgRole.canWrite`) y por `withApiAuth({requireWrite: 'factura'})` que valida en endpoints con admin client.

**Defense-in-depth real**: 3 capas. (1) RLS BD bloquea Supabase JS directo. (2) `requireWrite` en `withApiAuth` bloquea endpoints. (3) UI hook esconde botones (UX, no autoridad). Single test source garantiza coherencia: si añades resource, tocas SQL + role-matrix.ts + test vitest. Ver [[ADR-008-matriz-permisos-rol-aware-bd]] y [[rls-multi-tenant-limit-1-sin-order-bug-latente]].
