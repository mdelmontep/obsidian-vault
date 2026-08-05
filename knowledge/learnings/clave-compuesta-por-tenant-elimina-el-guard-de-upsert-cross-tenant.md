---
title: clave única compuesta (tenant_id, business_key) desde el diseño elimina el guard de upsert cross-tenant
date: 2026-08-05
source: claude-code-session
tags: [postgres, multi-tenant, schema-design]
---

Alternativa estructural a [[guard-cross-tenant-do-update-where-tenant-id-toctou]]: ese guard
(`WHERE tabla.tenant_id = EXCLUDED.tenant_id` + comprobar `rowCount`) solo hace falta cuando la
clave única ya es global y cruza tenants por diseño (caso Holded: `(channel, external_id)` sin
tenant_id en la clave).

Si en cambio el índice único se diseña compuesto **`(org_id, business_key)`** desde el primer
commit de la tabla, el problema desaparece por construcción: el propio target de `ON CONFLICT`
no puede alcanzar la fila de otra organización, así que no hace falta ningún guard aplicado en
cada escritura — un `INSERT` simple basta, y un conflicto solo puede darse dentro de la misma
organización.

Caso real (TuCRMIA, issue 020): `contacts` con `UNIQUE(org_id, phone_e164)` en vez de
`UNIQUE(phone_e164)` + guard. Regla al diseñar cualquier tabla multi-tenant con clave de negocio:
decidir la composición del índice único ANTES de escribir el upsert — si se puede componer con
`org_id` desde el diseño, hacerlo siempre gana al guard defensivo después.
