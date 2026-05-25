---
title: skip de validación SOLO en INSERT, nunca en UPDATE — vector evasión
date: 2026-05-21
source: claude-code-session
tags: [postgres, triggers, seguridad]
---

Si un trigger BEFORE hace skip de validación basado en un valor de input
(`metodo='automatico'`, `source='system'`, etc.), un user con permiso
UPDATE puede setear ese valor manualmente vía supabase-js cliente
directo y evadir todas las validaciones siguientes.

Caso real: mig 138 TuFacturaIA skipeó `mfa_no_overpayment` para
`metodo='automatico'` (mirror trigger creaba mfa que excedía total
fiscalmente OK). Vector evasión inmediato: user con role escritura
hace `UPDATE mfa SET importe=99999, metodo='automatico'` → bypass.

Patrón seguro: discriminar por `TG_OP`:
```sql
IF TG_OP = 'INSERT' AND NEW.metodo = 'automatico' THEN
  RETURN NEW; -- mirror/cron trigger fiable solo en INSERT
END IF;
-- UPDATE siempre se valida
```

Si necesitas skip también en UPDATE para casos legítimos, exigir que
OLD.metodo era ya 'automatico' (no transición INSERT-creator).
