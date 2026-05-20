---
title: Reescribir trigger que asume columna existente — verifica `information_schema.columns` antes
date: 2026-05-20
source: facturaia mig 111 (F5 fecha_pago)
tags: [postgres, triggers, schema-drift, migrations]
---

# Síntoma

Mig 111 reescribió 4 triggers de conciliación para setear `facturas.fecha_pago = mb.fecha` (simétrico a `fecha_cobro`). La migración aplicó OK porque CREATE OR REPLACE FUNCTION valida sintaxis pero NO valida que las columnas referenciadas existan (binding deferred a runtime).

Días después, primer INSERT en `movimientos_bancarios` con la feature → trigger ejecuta → `column "fecha_pago" does not exist` → INSERT abortado → import CSV vuelve `imported:0` con error críptico.

# Causa

`facturas.fecha_cobro` (mig 034) existía para emitidas pero `fecha_pago` para recibidas era una **asimetría histórica nunca arreglada**. Yo asumí simetría sin verificar.

# Regla

**Antes de escribir un trigger/función que toca columnas nuevas o "obvias" — `information_schema.columns` o `\d tabla` en psql**. CREATE FUNCTION es lazy, no falla en CREATE.

```sql
-- Antes de tocar el trigger:
SELECT column_name FROM information_schema.columns
 WHERE table_schema='public' AND table_name='facturas'
 ORDER BY column_name;
```

# Fix correcto

Mig hotfix con `ALTER TABLE ADD COLUMN IF NOT EXISTS fecha_pago DATE` + backfill desde `pagada_con_movimiento_id` + index parcial. NO usar workaround `as`/`COALESCE` ni try-catch.

# Aplicable a

- Cualquier reescritura de trigger SECURITY DEFINER.
- RPCs que referencian columnas asumidas.
- Mig de "simetría" que extiende patrón existente.

Relacionado: [[unique-index-concurrently-parcial-para-idempotencia-bd]]
