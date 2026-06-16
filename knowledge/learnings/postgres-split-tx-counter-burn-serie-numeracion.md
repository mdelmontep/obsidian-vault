---
title: postgres split-tx quema contadores de serie numeracion
date: 2026-06-08
source: claude-code-session
tags: [postgres, supabase, numeracion, transacciones]
---

Patrón roto: RPC `next_invoice_number_for_org` incrementa contador en TX1 (autocommit), INSERT del documento en TX2. Si TX2 falla, TX1 ya commitió → número quemado → hueco en la serie.

Caso prod TuFacturaIA 2026-06-08: facturas A2026-0001, 0002, 0021, 0028, 0031 (huecos por errores de inserción y retries del portal Agentesia).

Fix: mover el incremento DENTRO del RPC que hace el INSERT.

```sql
select id, formato into v_serie_id, v_formato
  from series_numeracion
 where org_id = p_org_id and codigo = p_serie and activa = true
 for update;                          -- bloquea contra concurrencia
update series_numeracion set contador_actual = contador_actual + 1
 where id = v_serie_id returning contador_actual into v_contador;
-- INSERT del documento aquí, misma transacción
```

Si el INSERT falla, Postgres rollbackea también el `UPDATE contador_actual`. Sin huecos.

Aplica a cualquier sistema de numeración secuencial (facturas, pedidos, tickets, matrículas).

**Variante 2026-06-16 (preview UI quema contador):** el form `/generar` llamaba a `next_invoice_number` (que hace `UPDATE contador+=1`) solo para *mostrar* el número → abrir "Nueva factura" sin guardar quemaba número. Fix: RPC `peek_invoice_number` read-only (`STABLE`, `SELECT contador+1`, sin UPDATE/FOR UPDATE); el número real lo asigna el INSERT (mig 299, PR #268). Regla: **un preview de numeración nunca debe consumir el contador**.
