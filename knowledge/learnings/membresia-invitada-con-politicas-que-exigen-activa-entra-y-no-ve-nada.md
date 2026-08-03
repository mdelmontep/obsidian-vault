---
title: una membresía «invitada» con políticas que exigen «activa» entra y no ve nada, sin un solo error
date: 2026-08-03
source: claude-code-session
tags: [supabase, rls, multi-tenant, onboarding]
---
Si las políticas de RLS llevan `and m.status = 'active'` y el alta crea la membresía como `'invited'`,
el usuario entra con sesión válida y la aplicación le enseña **cero filas**. Sin error, sin 403: la
consulta es correcta y devuelve vacío.

Antes de elegir el estado inicial de una membresía, mirar qué exigen las políticas. Y si el flujo de
aceptación no existe todavía, `'invited'` es un usuario atrapado: nadie lo pasa a `'active'`.

El consentimiento explícito (invitar a un tercero desde dentro del producto) y el alta que ejecuta el
proveedor para un cliente que ya contrató son **casos distintos**: el segundo puede nacer activo, con
`invited_email`/`invited_at` como rastro de por dónde entró.

Familia del fallo mudo: la lista vacía que devuelve 200. Ver [[rls-multi-org-active-vs-membership]]
