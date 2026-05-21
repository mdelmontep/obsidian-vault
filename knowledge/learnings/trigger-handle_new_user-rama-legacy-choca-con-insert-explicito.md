---
name: trigger-handle_new_user-rama-legacy-choca-con-insert-explicito
description: Triggers BD que auto-insertan al crear user chocan con flows nuevos que también insertan
metadata:
  type: feedback
---

Cuando cambias el modelo de dominio (ej. invitación: viejo "existing user → activo directo" → nuevo "consent-explícito → pending"), audita los triggers BD que duplican trabajo. El trigger `handle_new_user` en FacturaIA tenía rama legacy: si `raw_user_meta_data.invited_to_org_id` viene → INSERT membership `estado='activo'`. Con el modelo nuevo, el endpoint `POST /api/team/members` hace su propio INSERT `estado='invitado'` → choque UNIQUE (org_id, user_id) → 500 "duplicate key".

**Why:** Caso real 2026-05-21 — endpoint daba 500 al invitar email nuevo. El log decía `duplicate key value violates unique constraint "org_members_org_id_user_id_key"`. La causa NO era race condition propia ni FK rota — era trigger SECURITY DEFINER que insertaba antes que el endpoint. Reproducir con `pg_get_functiondef` reveló la rama.

**How to apply:** Tras refactor de flow de creación de entidad multi-tabla, `SELECT pg_get_functiondef(oid) FROM pg_proc WHERE proname='handle_new_user'` (o equivalente) y verifica que los triggers no dupliquen el trabajo del endpoint. Si lo hacen, decide: (a) quitar rama trigger (mejor — endpoint mantiene control), (b) endpoint con `ON CONFLICT DO NOTHING` (más defensivo pero ofusca quién manda). Ver [[matriz-permisos-rol-aware-bd-mas-espejo-ts]] para patrón "single source of truth".
