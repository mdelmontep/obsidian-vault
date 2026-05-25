---
title: rls multi-org usar get_user_org_id() no IN (SELECT org_members)
date: 2026-05-25
source: claude-code-session
tags: [supabase, rls, postgres, multi-org]
---

Bug TuFacturaIA 2026-05-25: en `/conciliacion` el user veía movimientos de TODAS sus orgs en lugar de solo la org activa. Causa: 16 tablas con RLS escrita así:

```sql
CREATE POLICY x ON tabla FOR SELECT USING (
  org_id IN (SELECT org_id FROM org_members WHERE user_id = auth.uid())
);
```

Si el user es miembro de N orgs (Manu de 4: AgentesiaLab, sandbox, tecnocloud, Borja Galván), esa policy permite leer filas de las N orgs. La "org activa" del switcher es solo UI — sin filtro explícito en query del cliente, RLS no la respeta.

**Patrón correcto** (mig 121 introdujo helper, mig 163 fixeó las 16 tablas legacy):

```sql
CREATE POLICY x ON tabla FOR SELECT USING (
  org_id = public.get_user_org_id()
);
```

`get_user_org_id()` lee `profiles.active_org_id` con validación de membresía activa (fallback determinista a primera membresía por `invited_at ASC`).

Para WRITE: combinar con `user_can_write_in_org(org_id, recurso)` o `current_org_role() IN ('propietario','admin','contable')`. Recurso registrado en matriz canónica (mig 121).

**Regla**: cualquier tabla per-org con app multi-org debe usar la función active-org, no la subquery membership. Validar en review de mig nueva.
