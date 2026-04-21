---
title: facturaia profiles tabla vacia trigger signup
date: 2026-04-21
source: claude-code-session
tags: [facturaia, supabase, pendiente]
---

La tabla `profiles` esta vacia porque no hay trigger que la popule al registrar un usuario.

Necesario: trigger `ON INSERT` en `auth.users` que cree fila en `profiles` con `user_id`, `email`, `is_superadmin = false`.

Mientras tanto, superadmin funciona via `SUPERADMIN_EMAILS` env var (fallback en `isSuperadmin()`). Pero para que `is_superadmin` en BD funcione, primero debe existir el row.

Resolver cuando se implemente el flujo de signup/onboarding real.
