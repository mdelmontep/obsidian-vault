---
title: on delete set null en fk compuesta anula todas las columnas, incluida la tenant not null
date: 2026-07-29
source: claude-code-session
tags: [postgres, fk, multi-tenant, supabase]
---
Una FK compuesta `(org_id, delegacion_id) REFERENCES padre (org_id, id) ON DELETE SET NULL`
no anula solo la columna que apunta al padre: anula **todas** las del constraint.
Como `org_id` es `NOT NULL` (patrón anti-IDOR, ver
[[fk-compuesta-tenant-id-defensa-multi-tenant-estructural]]), borrar el padre revienta
con `23502 null value in column "org_id"` en vez de dejar al hijo huérfano-pero-vivo.

No se ve en tests (nadie borra un padre) ni en el `db push`: la migración aplica
perfecta y el fallo aparece meses después, la primera vez que alguien borra una fila.

Fix (Postgres 15+): acotar la columna que se anula.
`FOREIGN KEY (org_id, delegacion_id) REFERENCES padre (org_id, id) ON DELETE SET NULL (delegacion_id)`

Al escribir una FK compuesta, elegir el `ON DELETE` mirando la columna tenant:
`CASCADE` suele ser lo correcto si el hijo no tiene sentido sin el padre; `SET NULL`
solo con la sintaxis de columna. Caso real: TuFacturaIA mig 583→585, tabla `contactos`.
