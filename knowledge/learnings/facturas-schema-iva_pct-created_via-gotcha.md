---
title: Tabla `facturas` — gotchas schema (iva_pct, created_via NOT NULL con CHECK)
date: 2026-05-23
source: seed dirigido bullet IA cashflow v2 en sandbox
tags: [supabase, postgres, schema, seeding, gotcha]
---

## Contexto

Al sembrar facturas dummy desde SQL en sandbox (smoke bullet IA cliente paga tarde), 2 INSERT fallaron consecutivamente por errores de schema no obvios.

## Gotchas

### 1. La columna IVA-amount no existe — usar `iva_pct`

```sql
-- ❌ FAIL: ERROR: column "iva" of relation "facturas" does not exist
INSERT INTO facturas (..., base, iva, total, ...) VALUES (..., 1000, 210, 1210, ...);

-- ✅ OK
INSERT INTO facturas (..., base, iva_pct, total, ...) VALUES (..., 1000, 21, 1210, ...);
```

El IVA no se almacena como importe sino como **porcentaje** (`iva_pct NUMERIC(5,2) DEFAULT 21`). El importe del IVA se calcula al vuelo como `total - base`. Coherente con todo el código (`fiscal-forecast.ts`, PDFs, conversión presupuesto, etc.).

### 2. `created_via` es NOT NULL con CHECK constraint

```sql
-- ❌ FAIL: null value in column "created_via" violates not-null constraint
INSERT INTO facturas (id, org_id, ..., serie, created_at) VALUES (...);

-- ❌ FAIL: new row violates check constraint "facturas_created_via_check"
INSERT INTO facturas (..., created_via, ...) VALUES (..., 'manual', ...);
```

`created_via` NOT NULL **sin DEFAULT**, con CHECK que solo permite 4 valores. Verificable:

```sql
SELECT DISTINCT created_via FROM facturas WHERE created_via IS NOT NULL;
-- → voice / email / web / api
```

`'manual'` NO está en el CHECK (aunque la columna legacy `fuente` sí acepta `'manual'`). Para seed manual desde SQL usar `'web'`:

```sql
-- ✅ OK
INSERT INTO facturas (..., created_via, ...) VALUES (..., 'web', ...);
```

## Por qué

`created_via` lo introdujo la mig de audit actor (`039_audit_actor_externo.sql`) para distinguir el canal de creación con vistas join sobre `api_keys.created_via_api_key_id`. Los 4 valores cubren los canales legítimos de creación; `'manual'` queda en `fuente` (columna previa) que sí admite ese valor.

## Patrón seed dirigido reusable

Para sembrar facturas históricas con `fecha_cobro` (smoke patterns / cashflow / fiscal), el INSERT mínimo viable:

```sql
INSERT INTO facturas (
  id, org_id, cliente_id, tipo, num, fecha, vto, fecha_cobro,
  base, iva_pct, total, estado, serie, created_via, created_at
) VALUES (
  gen_random_uuid(), '<org_uuid>'::uuid, '<cliente_uuid>'::uuid, 'emitida',
  'SMOKE-XX-1', '2026-01-31', '2026-03-02', '2026-04-16',
  1000, 21, 1210, 'cobrada', 'A', 'web', now()
);
```

`generate_series` con `INSERT INTO ... SELECT` también funciona, pero los `RAISE EXCEPTION` del trigger no salen del `DO $$` hasta que termine — debug más lento. Para 4-5 rows mejor `VALUES (...), (...), (...)`.

Cleanup siempre con prefijo único:
```sql
DELETE FROM facturas WHERE num LIKE 'SMOKE-XX-%';
```

## Cross-ref

- mig 001 schema base `facturas`.
- mig 039 introduce `created_via` + CHECK.
- mig 113 añade `fecha_pago` (recibidas) — simétrico de `fecha_cobro` (emitidas) y triggers de mig 111.
