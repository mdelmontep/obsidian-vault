---
title: BD — UNIQUE INDEX CONCURRENTLY parcial para idempotencia anti-race
date: 2026-05-19
source: facturaia auditoría cruzada Sprint 3
tags: [postgres, supabase, idempotencia, race-condition, fiscal]
---

Para garantizar idempotencia ante operaciones concurrentes (ej. dos clicks rápidos a "Anular" o dos requests paralelos creando el mismo recurso), un advisory lock de aplicación es **insuficiente** porque no sobrevive a sesiones distintas. La solución correcta es un **constraint a nivel BD**.

Patrón:
```sql
CREATE UNIQUE INDEX CONCURRENTLY IF NOT EXISTS uniq_abono_por_factura_origen
  ON facturas (factura_origen_id)
  WHERE tipo_documento = 'abono' AND factura_origen_id IS NOT NULL;
```

- **CONCURRENTLY**: no bloquea writes durante creación. Va FUERA de BEGIN/COMMIT (Postgres lo exige).
- **Partial WHERE**: solo aplica a abonos con `factura_origen_id` no nulo, no afecta facturas regulares.
- **IF NOT EXISTS**: idempotente al re-aplicar.

En la app TS, envolver el `INSERT` en `try/catch` y al recibir SQLSTATE 23505 (`unique_violation`), re-leer el registro ganador y devolverlo idempotentemente con audit `race_resolved:true`:

```ts
try {
  const result = await createAbono(...)
  return result
} catch (err) {
  if (isUniqueViolation(err)) {
    const existing = await loadExistingAbono(orgId, facturaId)
    if (existing) return buildIdempotentResult(existing)
  }
  throw err
}
```

**Smoke previo crítico** antes de aplicar:
```sql
SELECT factura_origen_id, COUNT(*) FROM facturas
  WHERE tipo_documento='abono' AND factura_origen_id IS NOT NULL
  GROUP BY 1 HAVING COUNT(*) > 1;
```
Si hay filas violando el constraint, `CREATE INDEX CONCURRENTLY` falla dejando índice INVALID que hay que `DROP` antes de reintentar.

Caso real TuFacturaIA: mig 097 + `anularFactura` resolver SQLSTATE 23505. Cierra A-fiscal #8 (race concurrente dos POST a `/api/facturas/[id]/anular`). Complementa [[verifactu-rpc-atomico-cierra-race-transacciones-rest-separadas]] que cierra el race en path normal.

**Variante "cron idempotente vía 23505"** (Centro Fiscal mig 150): el cron `fiscal-avisos` insertaba `(declaracion_id, tipo)` esperando el conflict para skip silencioso, **pero el UNIQUE no existía** → duplicados activos. Patrón obligatorio en cualquier cron que escribe filas idempotentes: el cron asume el constraint, el constraint DEBE existir. Auditar con `\d+ tabla` en psql que el índice está antes de confiar en el catch 23505.

**Límite (audit 06-26): si la condición del WHERE vive en OTRA tabla, un partial unique NO puede expresarla.** Caso SEPA cobro: "factura con cobro en vuelo" = tiene línea SIN devolución cruzada, pero "devuelta" está en `sepa_devoluciones`, no en `sepa_remesa_lineas` → no se puede `WHERE no_devuelta`. Salida sin denormalizar: `pg_advisory_xact_lock(org)` + guard `IF EXISTS(...) RAISE unique_violation` DENTRO de la RPC atómica (mig 393). El lock serializa por org; la 2ª llamada espera el COMMIT de la 1ª y ya ve sus líneas. Misma familia que [[verifactu-rpc-atomico-cierra-race-transacciones-rest-separadas]].

**Límite 2 (3-sep-2026, mig 818 de facturaia): `CONCURRENTLY` NO cabe en `supabase db push`.** El CLI corre cada migración en un pipeline/transacción y `CREATE/DROP INDEX CONCURRENTLY` falla con SQLSTATE 25001 a mitad de fichero. Consecuencia medida: el DDL transaccional anterior quedó aplicado, la 818 sin registrar en `schema_migrations`, y el índice viejo marcado `indisvalid=false`: **sin UNIQUE en vigor** hasta el segundo push. El patrón de arriba (mig 097) funcionó porque se aplicó a mano; en una migración de `db push` el swap va **dentro** del `BEGIN/COMMIT`, sin CONCURRENTLY, con un `DO` que compruebe `pg_index.indisvalid` y el predicado antes del `COMMIT` (mig 806 ya lo decía en su cabecera; la 818 lo reaprendió). El coste, un lock de escritura de milisegundos en una tabla de 2.400 filas; a cambio no hay ventana sin UNIQUE. Dry-run en prod con ROLLBACK no lo detecta: el dry corta antes del COMMIT y lo de después nunca se ejecuta. Ver [[migracion-aplicada-fuera-de-historial-supabase]].
