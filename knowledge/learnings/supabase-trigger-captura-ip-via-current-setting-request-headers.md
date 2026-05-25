---
title: trigger Supabase captura IP/UA via current_setting('request.headers')
date: 2026-05-19
source: claude-code-session
tags: [supabase, postgres, audit, security]
---

En triggers PL/pgSQL `SECURITY DEFINER`, `current_setting('request.headers', true)::jsonb` devuelve los headers HTTP del request original cuando viene de PostgREST/Supabase REST. Permite escribir `audit_log` con IP/UA reales sin pasarlos como parámetro desde la app.

Patrón:
```sql
DECLARE v_headers jsonb; v_ip text;
BEGIN
  BEGIN
    v_headers := current_setting('request.headers', true)::jsonb;
    v_ip := coalesce(
      v_headers->>'cf-connecting-ip',
      split_part(v_headers->>'x-forwarded-for', ',', 1),
      v_headers->>'x-real-ip'
    );
  EXCEPTION WHEN OTHERS THEN v_ip := NULL;
  END;
  -- INSERT INTO audit_log ... (ip, detalles->>'user_agent', ...)
END;
```

El `BEGIN…EXCEPTION` envuelve porque en SQL directo (psql, cron, migrations) el GUC no existe y `current_setting` con `true` devuelve NULL — pero el cast `::jsonb` de NULL falla. Wrap = idempotente.

Combinar con `auth.uid()` para user_id y `coalesce(v_user_id IS NULL → 'service_role_or_migration')` como changed_via. Cubre auditoría regulatoria (AEAT, GDPR) sin tocar capa app.

Caso real: TuFacturaIA mig 095 — toggle Verifactu, trigger AFTER UPDATE en `organizations`.
