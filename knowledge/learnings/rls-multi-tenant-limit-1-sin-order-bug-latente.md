---
name: rls-multi-tenant-limit-1-sin-order-bug-latente
description: En Supabase RLS multi-tenant, SELECT ... LIMIT 1 sin ORDER BY = lookup arbitrario. Funciona "por accidente" cuando N=1; con N≥2 lee datos de la tenant equivocada.
date: 2026-05-20
source: claude-code-session
tags: [postgres, rls, supabase, multi-tenant]
---

Patrón habitual en helpers RLS y resolvers TS: `.from('org_members').limit(1).single()` o `SELECT org_id FROM org_members WHERE user_id=auth.uid() LIMIT 1`. Postgres devuelve "el que toque" según planner — sin garantía estable. Mientras cada user tiene 1 sola tenant funciona; al introducir multi-org el bug es inmediato y silencioso.

**Casos detectados TuFacturaIA (mig 120-121)**: `get_user_org_id()` SQL, `getOrgId` y `getSessionActor` TS, `whatsapp-resolve.resolveSenderOrgForUser`, `resolvePhoneChangeMatch` (bucket pending_change_old). Cada uno resolvía org arbitraria — RLS leía/escribía en la "no elegida".

**Fix canónico**: ORDER BY columna estable (`invited_at ASC`, `created_at ASC`) en el fallback. Mejor aún: fuente de verdad explícita (`profiles.active_org_id` UUID FK con default NULL, escrito por endpoint `/api/auth/switch-org` con audit log). Helpers SQL y TS comparten el mismo path via función `resolve_active_org(uid)`. Ver [[matriz-permisos-rol-aware-bd-mas-espejo-ts]].

**Recurrencia 2026-06-19 (#429)**: el `getOrgId` **cliente** de Settings (`src/components/settings/_shared.tsx`) seguía con `.limit(1).single()` pese a haberse arreglado el server en mig 120 — había DOS `getOrgId`. Toda la página de Settings cargaba/guardaba la org equivocada en multi-org. Lección: al matar este patrón, **grep TODOS los helpers homónimos/duplicados** (`grep -rn "getOrgId\|limit(1)"`), no solo el canónico.
