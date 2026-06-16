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
Recurrencia (FacturaIA `facturas.fuente`, hotspot): mismo bug 2× en días —
mig 313 añadió `'web'` (form web) y mig 315 `'copiloto'` (tool `emitirFactura`).
Cada canal nuevo que pasa `createDocument({source})` exige ampliar
`facturas_fuente_check`. Matiz nuevo (caso 'copiloto' 2026-06-17): un **smoke de
solo `preview` NO ejercita el `commit`** → el CHECK violado se escondió tras un
preview smoke verde; el bug salió LIVE. Regla: en tools con split preview/commit,
el smoke DEBE llegar al commit (ejecutar `executeTool(...,{userConfirmed:true})`,
no solo `preview`).
Relacionado: [[supabase-insert-silencioso-con-ts-nocheck-oculta-columnas-inexistentes]] · [[smoke-insert-directo-no-ejerce-el-motor-real]].
