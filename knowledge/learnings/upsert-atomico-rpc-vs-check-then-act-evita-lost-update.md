---
title: UPSERT atómico con RPC vs check-then-act para counters compartidos
date: 2026-05-24
source: FacturaIA mig 158 conciliacion_reglas_upsert
tags: [postgres, concurrency, race-conditions]
---

# UPSERT atómico (RPC) vs check-then-act para counters compartidos

Patrón antipattern que aparece a menudo en endpoints REST sobre Supabase:

```typescript
// Anti-pattern
const { data: existing } = await admin
  .from('tabla')
  .select('id, contador')
  .eq('clave', key)
  .maybeSingle()

if (existing) {
  await admin.from('tabla').update({ contador: existing.contador + 1 }).eq('id', existing.id)
} else {
  await admin.from('tabla').insert({ clave: key, contador: 1 })
}
```

Dos concurrent requests con la misma `key`:

- **Lost update**: ambos leen `existing.contador = 5`, ambos escriben `6`. Debería ser `7`.
- **Unique violation**: en INSERT path, ambos no encuentran existing → ambos intentan INSERT → uno falla con 23505. El cliente ve error pero la fila SÍ se creó. UX rota.

## El fix: una sola RPC atómica con ON CONFLICT

```sql
CREATE OR REPLACE FUNCTION public.tabla_upsert(
  p_clave TEXT,
  p_user_id UUID
) RETURNS public.tabla
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  v_result public.tabla;
BEGIN
  INSERT INTO public.tabla (clave, contador, created_by)
  VALUES (p_clave, 1, p_user_id)
  ON CONFLICT (clave)
  DO UPDATE SET contador = public.tabla.contador + 1
  RETURNING * INTO v_result;
  RETURN v_result;
END;
$$;
```

Desde el endpoint:

```typescript
const { data, error } = await admin.rpc('tabla_upsert', { p_clave, p_user_id })
```

Postgres garantiza atomicidad: el `ON CONFLICT DO UPDATE` se ejecuta dentro del mismo lock que el INSERT. No hay ventana entre SELECT y INSERT.

## Por qué NO basta con Supabase `.upsert()`

`supabase.from('tabla').upsert(..., { onConflict: '...' })` también usa `ON CONFLICT` pero el comportamiento del UPDATE es **sobrescribir todos los campos del payload**. Si envías `{ contador: 1, ... }`, en colisión PG hace `SET contador = 1` (overwrite, NO incrementa). Para incrementar necesitas:

- Una expresión SQL `contador = tabla.contador + 1` que Supabase REST API no soporta directamente.
- O leer primero y enviar `contador + 1` — vuelta al lost-update.

Por eso la RPC con función plpgsql es la solución correcta. La expresión `excluded.contador + 1` o `tabla.contador + 1` SOLO está disponible en SQL crudo.

## Cuándo aplicar

- Cualquier counter shared (veces_confirmada, num_uses, hits, etc.).
- Cualquier UPSERT donde necesitas lógica de "mezcla" diferente a overwrite (last_seen vs first_seen, max(x), array_append, jsonb_set).

## Fallback strategy

Si la RPC se introduce en una mig posterior a algunos deploys, el endpoint puede tener fallback:

```typescript
const { data: viaRpc, error: rpcErr } = await admin.rpc('tabla_upsert', { ... })
if (rpcErr) {
  // Mig 158 no aplicada todavía — usa upsert nativo (no incrementa pero al menos no falla)
  const fallback = await admin.from('tabla').upsert({ ... }).select('*').single()
  return fallback
}
```

Esto da resiliencia durante rolling deploy. Pero el fallback DEBE marcar warning a logs porque pierde la atomicidad.

## Conexión

Va con [[defense-in-depth-estado-activo-cuando-admin-client-bypasa-rls]] — ambos son patrones para mutaciones seguras desde service-role.
