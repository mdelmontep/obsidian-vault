---
title: ADR-009 — Invitaciones con consent explícito (estado='invitado') vs activo-directo para existing users
date: 2026-05-21
status: accepted
tags: [adr, facturaia, team, multi-org]
---

## Contexto
FacturaIA es SaaS multi-org: un user puede pertenecer a varias orgs (gestor externo, contable freelance). Modelo viejo: si el invitado YA tenía cuenta FacturaIA, el admin podía añadirlo `estado='activo'` directo sin que él aceptase. Solo recibía email "te han añadido". Bug latente: estados `'invitado'` nunca se promovían a `'activo'` (no había endpoint accept), aunque `withApiAuth` los aceptaba.

## Opciones consideradas
- **A — Activo directo para existing users** — rápido, sin fricción. Contra: el invitado no consciente; un admin de cualquier org podía meterte sin tu OK. Mal en B2B multi-org.
- **B — Consent explícito universal** — toda invitación crea `estado='invitado'` + email "Aceptar" + endpoint `POST /api/team/invitations/accept`. Toggle pending → activo solo cuando el invitado clica. Estándar Slack/Notion/Linear.
- **C — Híbrido (activo directo solo si misma "empresa" detectada por dominio email)** — heurística frágil, casos edge raros.

## Decisión
**B**, porque (1) coherente con SaaS multi-org real, (2) resuelve el bug latente de `'invitado'` forever stuck, (3) audit log más limpio con evento "aceptación" explícito, (4) privacy: ningún admin puede enchufarte a su org sin tu OK.

## Consecuencias
- Endpoint nuevo `POST /api/team/invitations/accept` (bypass OTP gate).
- Página `/invitacion` bifurcada: set password (signup) | botón Aceptar (existing).
- Trigger BD `handle_new_user` perdió la rama legacy `invited_to_org_id` (mig 130) — duplicaba el INSERT.
- RLS `org_members_select` ampliada con `OR user_id = auth.uid()` (mig 129) para que el invitado pueda leer su fila pending.
- Modelo Resend: email único `team-invite-email`. Borrado `team-added-existing-user-email`.
- Ver [[hash-magic-link-supabase-requiere-setsession-explicito]] + [[trigger-handle_new_user-rama-legacy-choca-con-insert-explicito]] + [[rls-org-members-select-debe-incluir-own-memberships]] + [[cookie-impersonate-leak-fuera-de-admin]].
