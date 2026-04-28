---
title: supabase inviteuserbyemail no siempre propaga data a raw user meta data
date: 2026-04-28
source: claude-code-session
tags: [supabase, auth, gotcha]
---

`admin.auth.admin.inviteUserByEmail(email, { data: { invited_to_org_id, ... } })` no siempre escribe el `data` en `raw_user_meta_data` que ve un trigger `handle_new_user`. Resultado: el trigger no crea el `org_member`, el usuario invitado no pertenece a ninguna org, login → loop de redirects.

## Patrón fiable

1. Tras `inviteUserByEmail`, capturar `data.user.id` y crear el `org_member` directamente con upsert: `estado: 'invitado'`, `rol`, `org_id`. NO depender del trigger.
2. En `getSessionActor`/lookup de org: aceptar org_members con `estado IN ('activo', 'invitado')`.
3. Al primer login del invitado, promover su `estado` a `'activo'`.

Así el listado de equipo lo muestra desde que se invita (con pill "Invitado"), y al confirmar password + entrar al dashboard, pasa a Activo automáticamente. Sin loops, sin filas fantasma, sin depender de un trigger frágil.
