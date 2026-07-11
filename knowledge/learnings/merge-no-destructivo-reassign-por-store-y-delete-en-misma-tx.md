---
title: fusionar 2 filas padre con hijos FK — reassign por-store + delete en la MISMA tx
date: 2026-07-11
source: claude-code-session
tags: [postgres, transactions, dedup, arquitectura]
---
Postgres no tiene "CASCADE UPDATE". Para fusionar dos entidades padre duplicadas (p. ej. dos clientes
que son la misma cuenta) SIN perder historial:

1. Reasignar el FK de cada tabla hija: `UPDATE hijo SET parent_id=canonico WHERE parent_id=dup`.
2. LUEGO borrar el duplicado.
3. **Todo en UNA transacción / la misma conexión.**

Gotcha peligroso: si el `DELETE` del duplicado corre en OTRA conexión que los `UPDATE`, su
`ON DELETE CASCADE` ve los hijos aún colgando del dup (los reassigns no están commiteados) y los
**borra en silencio** → pérdida de datos. Por eso el delete debe aceptar el mismo `tx` handle.

Diseño: cada store dueño reasigna su propia tabla (`reassignClient(tenant, from, to, tx)`); un
executor coordina con un `TransactionRunner`. Scope por `(tenant, parent_id)` = exactamente el set
que el cascade tocaría → ni huérfanos ni pérdida. (Caso real: `crm.mergeClients`, AGH #245.)
