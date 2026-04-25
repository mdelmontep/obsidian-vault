---
title: re-autenticacion con password para acciones sensibles admin
date: 2026-04-25
source: claude-code-session
tags: [seguridad, admin, supabase, ux]
---

Patron para proteger ediciones destructivas o de alto impacto en paneles admin SaaS multi-tenant.

## Flujo

1. **Campos bloqueados por defecto** — `disabled` + opacity reducida + banner de aviso explicando el impacto
2. **Boton "Desbloquear"** abre modal pidiendo contraseña del admin actual
3. **Verificacion server-side** via `supabase.auth.signInWithPassword({ email: user.email, password })` — re-autentica al usuario actual, no crea sesion nueva
4. **Si OK** → desbloquea inputs, muestra botones Guardar/Cancelar
5. **Al guardar o cancelar** → vuelve a bloquear

## Endpoint verify

```typescript
// POST /api/admin/config/verify
const { data: { user } } = await supabase.auth.getUser()
const { error } = await supabase.auth.signInWithPassword({
  email: user.email,
  password,
})
if (error) return NextResponse.json({ error: 'Invalid password' }, { status: 401 })
```

## Cuando aplicar

- Config global que afecta a todas las orgs (ej: numero WhatsApp compartido)
- Cambios de billing masivos
- Modificar API keys o tokens de integracion
- Toggle de features core que afectan produccion

## UX

- Banner naranja con icono warning antes de desbloquear
- Input password con autofocus + Enter para confirmar
- Estado `original` guardado para poder cancelar y revertir visualmente
- Boton Guardar deshabilitado si no hay cambios (`hasChanges`)
