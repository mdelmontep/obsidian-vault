---
title: insertar en auth.users a mano crea cuentas que no pueden entrar
date: 2026-08-03
source: claude-code-session
tags: [supabase, gotrue, auth, seeds, smoke]
---

Un `insert into auth.users (...)` por SQL crea una fila que **existe, aparece en el censo y no
puede iniciar sesión**. GoTrue contesta `500 Database error finding user` a `generate_link` y
a cualquier operación de administración sobre ella.

Causa: GoTrue lee varias columnas de token —`confirmation_token`, `recovery_token`,
`email_change`, `email_change_token_new`— en un `string` de Go, y un `insert` a mano las deja a
`NULL`. Además se salta los triggers y el hasheo de identidades.

**Las cuentas las crea GoTrue, siempre**: `POST /auth/v1/admin/users` con
`{ email, email_confirm: true }`, o `admin.createUser()`. El perfil y la membresía sí van por
SQL, que es además lo que se quiere cuando hay columnas privilegiadas que `authenticated` no
puede escribir.

Dónde muerde de verdad: en los **seeds de un smoke**. El script que iba a verificar el alta de
punta a punta fallaba en su segunda comprobación por sembrar así, y el síntoma —un 500 de
GoTrue— no apunta a la siembra.

Ver [[supabase-createuser-race-trigger-handle-new-user]] ·
[[enlace-de-acceso-canjeado-en-el-servidor-con-hashed-token]]
