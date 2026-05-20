---
name: supabase-createuser-race-trigger-handle-new-user
description: admin.auth.admin.createUser() dispara trigger handle_new_user síncrono que crea profile. Para invitaciones atómicas hay que ordenar createUser → INSERT membership → generateLink → email + rollback (deleteUser + delete membership) si email falla.
date: 2026-05-20
source: claude-code-session
tags: [supabase, auth, race-condition]
---

Patrón de invitación de equipo: querer crear user nuevo + asociarlo a una org + mandarle email con link de aceptación. Si `sendEmail` falla a mitad (Resend rate-limit, SMTP timeout), querer revertir todo.

**Orden estricto**: `createUser({email, email_confirm:false})` — esto dispara trigger `handle_new_user` síncrono que inserta profile vacío con default. → INSERT `org_members` con estado='invitado' + audit fields. → `generateLink({type:'invite'})` para action_link. → `sendTeamInviteEmail(actionLink)` con Resend. → si email falla, helper `rollback()` que hace `delete from org_members` Y `admin.auth.admin.deleteUser(userId)`.

**Sin rollback de auth.users**: quedaba cuenta zombie sin profile. Próxima invitación al mismo email devolvía `user_exists` → endpoint no podía recuperar sin intervención manual SQL. Solución de recovery: detectar mensaje `user_exists/already_registered`, re-query profile (puede haberse creado por race) y devolver 409 `user_exists_retry` pidiendo al cliente reintentar (esta vez caerá en rama de user existente).
