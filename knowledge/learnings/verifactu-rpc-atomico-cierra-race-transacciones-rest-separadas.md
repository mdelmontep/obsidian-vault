---
title: verifactu — RPC atómico cierra race transacciones REST separadas
date: 2026-05-19
source: facturaia auditoría cruzada Sprint 3
tags: [fiscal, aeat, supabase, postgres, transacciones, race-condition]
---

Si una función necesita ejecutar 2+ INSERTs en tablas con triggers que dependen entre sí (ej. `facturas` con trigger BEFORE INSERT que calcula huella + `lineas_factura` con trigger AFTER INSERT que la recalcula), hacerlos vía cliente REST Supabase **NO es atómico**: cada `admin.from('X').insert()` es su propia transacción.

Si hay un advisory_xact_lock en el primer trigger, **se libera al COMMIT del primer INSERT**, antes del segundo. Una transacción concurrente puede entrar entre ambos → race.

**Fix**: encapsular ambos INSERTs en un RPC SQL `SECURITY DEFINER`. El RPC es una transacción única; cualquier advisory_xact_lock adquirido dentro vive hasta el COMMIT del RPC entero, cubriendo todos los INSERTs y sus triggers.

Beneficio secundario: si el segundo INSERT falla, Postgres rollbackea atómicamente. Elimina la compensación manual con `DELETE` en TS (más limpio, más rápido).

Patrón:
```sql
CREATE OR REPLACE FUNCTION create_x_with_y(p_x JSONB, p_y JSONB)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public, extensions
AS $$
DECLARE v_id UUID;
BEGIN
  INSERT INTO x (...) VALUES (...) RETURNING id INTO v_id;
  INSERT INTO y (...) SELECT v_id, ... FROM jsonb_array_elements(p_y);
  RETURN jsonb_build_object('id', v_id);
END;
$$;
GRANT EXECUTE ON FUNCTION ... TO service_role;
```

TS: `admin.rpc('create_x_with_y', { p_x: {...}, p_y: [...] })`.

Tests: mockear `admin.rpc.mockResolvedValueOnce({ data: {...}, error: null })` en lugar de 2 `queueResponse` separados.

Caso real TuFacturaIA: mig 094 cerró race A-fiscal #2 entre INSERT facturas (huella `total-base`) e INSERT lineas (recálculo huella con Σ). Ver [[unique-index-concurrently-parcial-para-idempotencia-bd]] para el patrón hermano que blinda race a nivel de constraint.
