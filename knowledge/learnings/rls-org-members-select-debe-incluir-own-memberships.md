---
name: rls-org-members-select-debe-incluir-own-memberships
description: RLS de org_members filtrada solo por active_org_id bloquea flows multi-org (aceptar invitación, switch)
metadata:
  type: feedback
---

Si la policy SELECT de `org_members` filtra solo por `(org_id = get_user_org_id())`, el user no puede leer SUS PROPIAS filas en OTRAS orgs. Esto rompe:
- Aceptar invitación a una org distinta de la activa (la página `/invitacion` no encuentra su membership pending).
- Switch-org desde UI (no puede listar a qué orgs pertenece).
- Audit del propio user en multi-org.

**Why:** Caso real 2026-05-21 — flow aceptar invitación caía a "no_pending" porque el invitado existing tenía `active_org_id` en su org original; la fila 'invitado' en la nueva org era invisible por RLS.

**How to apply:** Policy correcta:
```sql
CREATE POLICY org_members_select ON public.org_members
  FOR SELECT
  USING (
    org_id = get_user_org_id()
    OR user_id = auth.uid()
  );
```
Seguro: solo expone TUS propias filas, no las de otros. Patrón general para tablas con `user_id`: el dueño SIEMPRE puede leer lo suyo, aunque la "org activa" no coincida. Vale también para `org_invitations`, `org_credentials_personal`, etc. Ver [[rls-multi-tenant-limit-1-sin-order-bug-latente]] para otro caso de RLS multi-tenant subóptima.
