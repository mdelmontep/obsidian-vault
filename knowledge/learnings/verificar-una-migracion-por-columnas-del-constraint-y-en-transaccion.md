---
title: verificar una migración por columnas del constraint y en transacción
date: 2026-08-24
source: agency-portal
tags: [postgres, migraciones, supabase-selfhosted, verificacion]
---
Tres fallos de una migración de endurecimiento que "verificaba contra catálogo" (24-ago, Flota IA):

1. **Verificar por nombre no discrimina.** `count(*) where conname='x_key'` da 0 tanto si el UNIQUE viejo murió como si sobrevive con otro nombre. Comprobar por **columnas**: `conkey` de `pg_constraint` resuelto contra `pg_attribute` (`array_agg(attname order by attnum)`), y exigir además el total de `contype='u'` esperado.
2. **`ON_ERROR_STOP=1` no revierte.** Sin `--single-transaction` o `BEGIN;/COMMIT;` en el fichero, el `RAISE EXCEPTION` del bloque `DO` de verificación salta con el DROP/ADD/REVOKE ya commiteados: queda a medias con mensaje de pánico. Envolver siempre.
3. **Idempotencia**: `ADD CONSTRAINT` sin `DROP … IF EXISTS <nombre nuevo>` antes → 42710 al reaplicar.

Bonus de privilegios de columna: `REVOKE SELECT ON tabla FROM authenticated` + `GRANT SELECT (cols)` hace que `select *` por PostgREST falle **entero** (42501), no que devuelva columnas parciales. Enumerar las columnas permitidas (fail-closed para columnas futuras) y verificar con `information_schema.column_privileges` filtrando `grantee='authenticated'` (la vista también lista `postgres`/`service_role`).
