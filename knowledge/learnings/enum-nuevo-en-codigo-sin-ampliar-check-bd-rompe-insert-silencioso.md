---
title: valor de enum nuevo en código sin ampliar el check de la bd rompe el insert en silencio
date: 2026-06-04
source: claude-code-session
tags: [postgres, supabase, observabilidad, anti-patron]
---
Añadir un valor a una unión TS (p.ej. `EmailLogKind += 'password_reset'`) sin
ampliar el CHECK de la columna en BD → el INSERT viola el constraint. Si el
INSERT es outbox-first (log antes de enviar), el fallo **aborta el envío
entero**: el email nunca sale, para TODOS los usuarios, no solo uno.
Agravante: si el endpoint responde genérico por seguridad (200 anti-enumeración
en recover-password), el fallo es invisible salvo en stdout. Llevaba roto sin
que saltara nada.
Detección: `SELECT pg_get_constraintdef` del `*_check` y cruzar con el tipo en
código. Evidencia: 0 filas del kind en la tabla de log pese a 200 en el flujo.
Fix: migración que re-crea el CHECK (idempotente DROP IF EXISTS + ADD). Regla
viva: "cambio de enum en código → grep consumidores + PATCH/CHECK en BD".
Y: respuesta genérica anti-enum necesita observabilidad interna aparte (alerta/
metric) que no dependa del status devuelto al cliente.
Relacionado: [[supabase-insert-silencioso-con-ts-nocheck-oculta-columnas-inexistentes]].
