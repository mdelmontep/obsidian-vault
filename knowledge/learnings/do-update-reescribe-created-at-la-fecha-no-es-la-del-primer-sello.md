---
title: do update reescribe created_at — la fecha de un idempotency_log no es la del primer sello
date: 2026-08-10
source: claude-code-session
tags: [postgres, idempotencia, diagnostico, metodo]
---
Diagnosticando por qué faltaban avisos (Elphis) leí `idempotency_log` y vi claves
`notif-recepcion-undefined` fechadas en junio. Conclusión inmediata y **falsa**: «esa clave está
quemada desde junio, lleva dos meses bloqueando avisos». Se lo dije al usuario como hallazgo grave.

La query era `INSERT ... ON CONFLICT (key) DO UPDATE SET expires_at=EXCLUDED.expires_at,
created_at=NOW() WHERE idempotency_log.expires_at < NOW() RETURNING key`. Dos cosas que la tabla
sola no dice: hay **ventana** (60 min, se re-reclama al expirar, no bloquea nunca para siempre) y
`created_at` se **reescribe** en cada reclamación, así que la fecha es la de la ÚLTIMA vez, no la
primera. Una fila vieja significa «no se ha vuelto a usar desde entonces» — lo contrario de lo que
leí.

**Regla:** el estado de un dedup no se interpreta desde su tabla, se interpreta desde su query.
Leer el `ON CONFLICT` antes de concluir; si hay `DO UPDATE`, ninguna columna de fecha es un
histórico. Casi «arreglo» un dedup que funcionaba bien.

Ver [[idempotencia-de-entidad-no-debe-gatear-notificacion-side-effect]] · [[n8n-status-success-no-implica-camino-critico]]
