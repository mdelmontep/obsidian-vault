---
title: workers concurrentes en outbox → RPC SECURITY DEFINER con FOR UPDATE SKIP LOCKED
date: 2026-05-29
source: claude-code-session
tags: [postgres, concurrency, outbox, rpc]
---

Workers múltiples pickeando outbox con `SELECT ... ORDER BY LIMIT` sin lock procesan filas duplicadas. Patrón seguro y limpio:

```sql
create function claim_batch(p_size int) returns table(...)
language plpgsql security definer set search_path = public
as $$
begin
  return query
    with picked as (
      select id from queue
      where status='pending' and next_retry_at <= now()
      order by priority asc, next_retry_at asc
      for update skip locked
      limit p_size
    )
    update queue q set status='processing', processing_started_at=now()
    from picked where q.id = picked.id
    returning q.*;
end; $$;
```

`SKIP LOCKED` evita que dos workers compitan por la misma fila. `SECURITY DEFINER` necesario si la tabla tiene RLS deny-all (caso típico outbox service-role-only). `revoke from authenticated/public` por higiene.

Webhook-dispatcher de TuFacturaIA NO usa este patrón — caveat documentado en su comentario porque su volumen es bajo. Para backfills grandes (~5k filas) sí hace falta. Cron tracking con `withCronTracking` añade lock distribuido a nivel de cron entero, complementario al SKIP LOCKED a nivel fila.
