---
title: una credencial de test guardada puede apuntar a otro proyecto y a un usuario sin membresías
date: 2026-07-28
source: claude-code-session
tags: [supabase, e2e, 1password, credenciales, testing]
---

El `.env.test` guardado en 1Password fallaba el login. Dos desalineaciones a la vez, y ninguna daba un error que lo dijera:

1. **Proyecto equivocado**: apuntaba a otro proyecto de Supabase que el que usa la app (`.env.local`). Se destapa mirando el `iss` del JWT que emite el propio proyecto, que lleva la ref dentro. Un `.env.example` del repo no vale como prueba: el suyo decía el proyecto correcto y el fichero real, no.
2. **Usuario sin membresías**: el usuario existía en `auth.users` del proyecto bueno, así que "existe", pero no era miembro de ninguna org. Login válido, aplicación inservible.

Al alinear, el usuario correcto era otro (el que aparecía con `last_sign_in_at` reciente en el proyecto que usa la app). Ese campo es el mejor indicio de cuál es la cuenta viva.

Regla: verificar una credencial de test contra las TRES cosas —proyecto, autenticación y **membresía en la org de pruebas**— y guardar el fichero completo, no solo la contraseña. Un ítem por entorno, sin reutilizar el de otra rama.

Caso real 2026-07-28, TuFacturaIA.
