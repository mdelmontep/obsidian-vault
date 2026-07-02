---
title: guard cross-tenant en upsert — DO UPDATE ... WHERE tenant_id = EXCLUDED + rowCount
date: 2026-07-02
source: claude-code-session
tags: [postgres, multi-tenant, concurrency]
---

Tabla con clave única **global** que cruza tenants (p.ej. `identities` PK `(channel, external_id)`, sin tenant_id en la PK). Un `INSERT ... ON CONFLICT DO UPDATE SET user_id=EXCLUDED.user_id` ciego permite que el tenant B "robe" una fila del tenant A al reasignarla.

Guard secuencial (`SELECT tenant_id` → si es de otro, throw) tiene **TOCTOU**: dos applies concurrentes pasan el SELECT y el DO UPDATE pisa igual.

Backstop atómico en la propia BD: `ON CONFLICT DO UPDATE SET user_id=EXCLUDED.user_id **WHERE tabla.tenant_id = EXCLUDED.tenant_id**` → si el conflicto es con otro tenant, 0 filas afectadas → comprobar `rowCount===0` y lanzar. Nunca se toca `tenant_id`, así que el recurso jamás cambia de dueño. Extiende [[upsert-atomico-rpc-vs-check-then-act-evita-lost-update]] al caso de aislamiento (no de counter).
