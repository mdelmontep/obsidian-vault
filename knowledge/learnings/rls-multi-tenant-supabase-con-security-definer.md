---
title: rls multi-tenant en supabase usa security definer para aislar org_id
date: 2026-04-19
source: claude-code-session
tags: [supabase, rls, multi-tenant, arquitectura]
---

## Patrón

Para SaaS multi-tenant en Supabase Cloud, el aislamiento se consigue con una función SECURITY DEFINER que resuelve el `org_id` del usuario autenticado. Todas las policies de RLS la referencian en vez de hacer joins directos.

## Función clave

```sql
CREATE OR REPLACE FUNCTION get_user_org_id()
RETURNS uuid
LANGUAGE sql
SECURITY DEFINER
STABLE
AS $$
  SELECT org_id FROM org_members WHERE user_id = auth.uid() LIMIT 1;
$$;
```

- `SECURITY DEFINER` = ejecuta con permisos del creador (service role), no del caller
- `STABLE` = Postgres puede cachear el resultado dentro del mismo statement
- Todas las tablas tienen columna `org_id uuid NOT NULL`

## Policies

Patrón uniforme para todas las tablas:

```sql
ALTER TABLE facturas ENABLE ROW LEVEL SECURITY;

CREATE POLICY "org_select" ON facturas FOR SELECT
  USING (org_id = get_user_org_id());

CREATE POLICY "org_insert" ON facturas FOR INSERT
  WITH CHECK (org_id = get_user_org_id());

CREATE POLICY "org_update" ON facturas FOR UPDATE
  USING (org_id = get_user_org_id());

CREATE POLICY "org_delete" ON facturas FOR DELETE
  USING (org_id = get_user_org_id());
```

## Onboarding

Función RPC para que el registro cree organización + membresía en una sola llamada:

```sql
CREATE OR REPLACE FUNCTION create_org_for_user(org_nombre TEXT)
RETURNS uuid
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE new_org_id uuid;
BEGIN
  INSERT INTO organizations (nombre) VALUES (org_nombre) RETURNING id INTO new_org_id;
  INSERT INTO org_members (org_id, user_id, rol) VALUES (new_org_id, auth.uid(), 'owner');
  RETURN new_org_id;
END;
$$;
```

## Auto-numeración con bloqueo

```sql
CREATE OR REPLACE FUNCTION next_invoice_number(serie_codigo TEXT)
RETURNS TEXT
LANGUAGE plpgsql
AS $$
DECLARE
  current_num INT;
  serie_row series_numeracion%ROWTYPE;
BEGIN
  SELECT * INTO serie_row FROM series_numeracion
    WHERE codigo = serie_codigo AND org_id = get_user_org_id()
    FOR UPDATE;  -- bloqueo de fila para concurrencia
  current_num := serie_row.siguiente;
  UPDATE series_numeracion SET siguiente = current_num + 1
    WHERE id = serie_row.id;
  RETURN serie_row.prefijo || LPAD(current_num::TEXT, 5, '0');
END;
$$;
```

## Por qué este patrón y no alternativas

- **JWT claims custom**: requiere edge functions para actualizar el token al cambiar de org. Más complejo.
- **Join directo en cada policy**: repite la lógica N veces, más propenso a errores.
- **Schema por tenant**: no escala en Supabase Cloud (no puedes crear schemas dinámicamente con RLS).

La función centralizada es el punto único de cambio si el modelo de membresía evoluciona (ej: múltiples orgs por usuario).

---

*Usado en: [[FacturaIA]] — 17 tablas con este patrón*
