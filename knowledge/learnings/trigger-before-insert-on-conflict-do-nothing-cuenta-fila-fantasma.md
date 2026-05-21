---
title: trigger BEFORE INSERT cuenta fila fantasma cuando hay ON CONFLICT DO NOTHING
date: 2026-05-21
source: claude-code-session
tags: [postgres, triggers, gotcha]
---

Si un trigger BEFORE INSERT valida sumas o estados sobre la tabla, y el
INSERT lleva `ON CONFLICT (cols) WHERE ... DO NOTHING`, el trigger se
ejecuta ANTES de la resolución del conflict. La fila intentada cuenta
para el SUM/COUNT del validator aunque ON CONFLICT la descarte → false
positive bloqueando flujos legítimos.

Síntoma típico: trigger A inserta una mfa, AFTER recompute → UPDATE
facturas → trigger mirror INSERT mfa idempotente con ON CONFLICT DO
NOTHING → BEFORE INSERT del validator suma fila A + fila fantasma →
overpayment falso.

Fix: skip validation si ya existe fila ACTIVA con misma clave UNIQUE:
```sql
IF TG_OP = 'INSERT' AND EXISTS (
  SELECT 1 FROM tabla WHERE clave_unique = NEW.clave_unique
    AND id <> COALESCE(NEW.id, gen_random_uuid())
) THEN RETURN NEW; END IF;
```

Detectado por smoke E2E tras 4 horas de smokes verdes — los triggers
unitarios pasaron, la composición trigger+mirror+ON CONFLICT falló.
Caso real: FacturaIA mig 137 (Conciliación).
