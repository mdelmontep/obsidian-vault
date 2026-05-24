---
title: Defense-in-depth — chequear estado='activo' explícito cuando admin client bypasea RLS
date: 2026-05-24
source: FacturaIA audit conciliación v3 mig 157
tags: [supabase, rls, security, multi-tenant]
---

# Defense-in-depth — `estado='activo'` cuando admin client bypasea RLS

Patrón frecuente en endpoints Next.js sobre Supabase:

```typescript
export const POST = withApiAuth({ ... }, async ({ orgId, userId, body }) => {
  const admin = createAdminClient()  // ← service_role, bypasea RLS
  await admin.from('tabla_compartida').upsert({ org_id: orgId, ... })
})
```

`withApiAuth` valida que el usuario tiene sesión y resuelve `orgId` desde `org_members`. Pero si la RLS de `tabla_compartida` solo filtra por membership sin chequear `estado='activo'`, el endpoint puede dejar mutar a:

- Usuarios invitados (membership creada pero todavía no aceptada).
- Usuarios bloqueados o despedidos (estado='inactivo' pero row no borrado por audit).
- Usuarios en período de gracia tras un rol downgrade.

El admin client bypasea TODO eso porque corre como `service_role`.

## El fix

Dos capas obligatorias:

**1. RLS con `estado='activo'`** en todas las policies:

```sql
CREATE POLICY tabla_select ON public.tabla_compartida
  FOR SELECT USING (
    org_id IN (
      SELECT org_id FROM public.org_members
      WHERE user_id = auth.uid() AND estado = 'activo'
    )
  );

-- Y lo mismo para INSERT/UPDATE/DELETE (USING + WITH CHECK).
```

**2. Defense-in-depth en endpoint** que use `createAdminClient()`:

```typescript
const admin = createAdminClient()
const { data: member } = await admin
  .from('org_members')
  .select('estado')
  .eq('user_id', userId!)
  .eq('org_id', orgId!)
  .maybeSingle()
if (member?.estado !== 'activo') {
  return NextResponse.json(
    { error: 'user_not_active_in_org' },
    { status: 403 },
  )
}
// ... ahora sí, mutación con admin
```

La RLS te cubre cuando el cliente usa `auth.uid()`. El check explícito te cubre cuando el endpoint usa service-role.

## Cuándo aplicar

A todo endpoint que:

1. Use `createAdminClient()` (service_role).
2. Mute tablas con datos compartidos en la org (configuración de módulos, reglas aprendidas, plantillas, settings de billing).

Casos típicos donde NO hace falta: endpoints que solo leen del propio usuario (`profiles.user_id = auth.uid()`), o endpoints que validan ownership por ID antes de mutar (factura.org_id == orgId).

## El truco que casi se cuela

En la auditoría de conciliación v3, la tabla `org_module_config` (creada en mig 045) tenía RLS pero las policies eran:

```sql
CREATE POLICY omc_modify ON public.org_module_config
  FOR ALL USING (
    org_id IN (SELECT org_id FROM public.org_members WHERE user_id = auth.uid())
  );
```

Sin `estado='activo'`. Funcionó durante meses porque solo usuarios activos llegaban al UI. Pero un test red-team: invitado con membership pendiente puede modificar config global de cashflow/conciliación de la org.

Fix aplicado en mig 157 + check explícito en endpoint cashflow/manual + reglas.

## Conexión

Va con [[upsert-atomico-rpc-vs-check-then-act-evita-lost-update]] — patrones de seguridad cuando se mezcla service-role con datos compartidos.
