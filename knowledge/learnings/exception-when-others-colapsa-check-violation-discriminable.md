---
title: EXCEPTION WHEN OTHERS colapsa check_violation discriminables → 500 opaco
date: 2026-05-21
source: claude-code-session
tags: [postgres, plpgsql, dx]
---

En una RPC plpgsql, `EXCEPTION WHEN OTHERS THEN ... db_exception` atrapa
también `check_violation` (sqlstate 23514) lanzados por triggers de
validación con `RAISE EXCEPTION 'mfa_overpayment...' USING ERRCODE`.
El endpoint mapea el genérico `db_exception` → 500 opaco al user
cuando el problema era contable claro (sobre-pago, tipo inválido).

Fix: discriminar antes del catch-all:
```sql
EXCEPTION
  WHEN unique_violation THEN ... -- 23505
  WHEN check_violation THEN
    IF SQLERRM LIKE 'mfa_overpayment%' THEN
      RETURN jsonb_build_object('ok', false, 'error', 'overpayment', ...);
    ELSIF SQLERRM LIKE 'mfa_tipo_invalido%' THEN
      RETURN jsonb_build_object('ok', false, 'error', 'tipo_invalido', ...);
    ELSE
      RETURN jsonb_build_object('ok', false, 'error', 'check_violation', 'sqlstate', SQLSTATE);
    END IF;
  WHEN OTHERS THEN ...
```

Endpoint mapea `overpayment`/`tipo_invalido` → 409 con detalle claro.
La convención `RAISE EXCEPTION '<error_code>: ...'` con prefijo
greppable hace el pattern match estable.

Caso real: FacturaIA RPC `confirmar_sugerencia` mig 141.
