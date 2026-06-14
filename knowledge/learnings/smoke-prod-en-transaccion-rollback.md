---
title: smoke de rpcs/triggers contra prod en transacción begin/rollback = cero residuo
date: 2026-06-14
source: claude-code-session
tags: [supabase, postgres, testing, smoke]
---
Para validar migraciones (RPCs, triggers, recompute) contra el schema REAL de
prod sin dejar datos ni escribir teardown: envolver todo en una transacción que
se revierte.

```
BEGIN;
DO $$ DECLARE v_org uuid; v_user uuid; ... BEGIN
  SELECT id INTO v_user FROM auth.users LIMIT 1;  -- user real (FK auth.users)
  INSERT INTO organizations(nombre,is_test) VALUES ('SMOKE-rollback',true) RETURNING id INTO v_org;
  -- ... crea factura/mov temp, llama las RPC, comprueba con IF ... RAISE EXCEPTION
END $$;
ROLLBACK;
```

- Cualquier aserción fallida (`RAISE EXCEPTION`) aborta; el `ROLLBACK` final no deja NADA aunque pase todo.
- Mejor que crear org sandbox + borrar al final: si el script peta a media, no hay residuo que limpiar.
- Las RPC no hacen llamadas externas → todo (mfa, triggers, module_events) entra en la txn y se revierte.
- `psql "$SUPABASE_DB_URL"` (de .env.local) o pooler; el `p_user_id` solo necesita existir en auth.users.
