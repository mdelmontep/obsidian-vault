---
title: invitar a crear org sin saber email exige token propio, no magic link supabase
date: 2026-05-28
source: claude-code-session
tags: [auth, multi-tenant, supabase, facturaia]
---

`inviteUserByEmail` / `generateLink({type:'invite'})` atan el `action_link` al
email concreto del invitado. Sirve para "invitar a una org existente" (email
conocido), pero NO para "te paso un link por WhatsApp y tú creas tu propia
org con el email que quieras".

Patrón: tabla `*_signup_invites` con token 32-hex + plan + trial_days +
expires_at. URL `/<registro>?invite=<token>`. La landing valida vía endpoint
público, `signUp` pasa el token en `options.data.signup_invite_token`, y el
callback de `/api/auth/callback` lo consume marcando `consumed_*` + aplicando
plan/trial a la org del nuevo propietario (la creó el trigger
`handle_new_user` en el INSERT a `auth.users`).

Consumo en código, NO en trigger SQL — `handle_new_user` ya es delicado.
RLS sin políticas (service-role-only). Best-effort: invite inválido en
último momento no bloquea el alta, el user acaba con plan default + log.

Diferenciar de [[auth-org-gate-bloquea-aceptar-primera-invitacion]] (invitar
a org existente) y [[supabase-inviteuserbyemail-no-propaga-data-a-raw-user-meta-data]].
