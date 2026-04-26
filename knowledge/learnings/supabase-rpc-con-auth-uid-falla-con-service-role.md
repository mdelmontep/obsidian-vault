---
title: supabase rpc con auth uid falla con service role
date: 2026-04-26
source: claude-code-session
tags: [supabase, rls, service-role, api-routes]
---

# Supabase RPCs con `auth.uid()` devuelven null con service_role key

Funciones SQL SECURITY DEFINER que internamente usan `auth.uid()` (como `get_user_org_id()`) devuelven null cuando se llaman desde `createAdminClient()` (service_role key).

**Por qué**: service_role bypasses RLS pero NO establece una sesión de usuario. `auth.uid()` requiere un JWT de usuario autenticado.

**Caso real**: `/api/voice/generate` usaba `admin.rpc('next_invoice_number', { serie: 'A' })` — la función internamente llama a `get_user_org_id()` que usa `auth.uid()` → null → no encuentra la serie → error 500.

**Fix**: queries directas con filtro `org_id` explícito en vez de RPCs que dependen de RLS:

```typescript
// MAL — falla con service_role
const { data } = await admin.rpc('next_invoice_number', { serie: 'A' })

// BIEN — query directa con org_id explícito
const { data } = await admin
  .from('series_numeracion')
  .select('id, contador_actual')
  .eq('org_id', org_id)
  .eq('codigo', 'A')
  .eq('activa', true)
  .single()
```

**Regla**: en API routes con `x-service-key` + `createAdminClient()`, nunca usar RPCs que dependan de `auth.uid()` internamente.
