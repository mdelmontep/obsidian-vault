---
title: componentes de settings que leen con createClient()/getOrgId() se rompen impersonando
date: 2026-06-24
source: TuFacturaIA PRs #457/#458/#460/#462 (logo de org no aparecía impersonando)
tags: [supabase, impersonacion, superadmin, rls, react, facturaia]
---

Un componente cliente que lee datos de org con `createClient()` (sesión real del superadmin) o `getOrgId()` (lee `profiles.active_org_id` del superadmin) **falla en silencio al impersonar**:

- `createClient().from('organizations').eq('id', orgImpersonada)` → **0 filas** por la RLS `org_member_select` (`id = get_user_org_id()`, y el superadmin no es miembro). El form sale vacío / logo como "?".
- `getOrgId()` devuelve la org ACTIVA del superadmin (no la impersonada) → carga datos de OTRA org. Caso real: la preview de Plantillas mostraba el logo de "FacturaIA Sandbox" (org del superadmin).

Fix: `useOrg().orgId` (la org impersonada, del OrgContext) + `useOrgClient()` (lecturas por el proxy `/api/admin/impersonate/query`, service_role acotado a la org). En sesión normal no cambia nada. Ojo: las escrituras del proxy siguen stub (read-only); Storage NO está en el proxy → subida via endpoint admin con service_role. Auditar TODA sección de Settings por este patrón.

Ver [[proxy-impersonacion-reimplementa-api-supabase-se-desincroniza]] · [[impersonacion-superadmin-no-sirve-para-qa-de-ui-org-scoped]].
