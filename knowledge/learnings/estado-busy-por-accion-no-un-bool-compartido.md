---
title: varios botones con un `busy` bool compartido ponen el label de progreso en el botón equivocado
date: 2026-07-10
source: claude-code-session
tags: [react, ui, frontend]
---
Barra/toolbar/modal con ≥2 acciones (aprobar, descartar, descargar, eliminar) que comparten UN
`const [busy,setBusy]=useState(false)` y hardcodean el label en cada botón (`busy ? 'Aprobando…' : …`):
al disparar UNA, TODOS los botones cambian de label a la vez → el progreso sale en el botón que NO
pulsaste, y el que sí pulsaste solo se atenúa sin señal. En modales mutuamente excluyentes no se ve
(un solo modal montado) pero es frágil.

Fix: estado POR-acción, no bool. `useState<'aprobar'|'descartar'|…|null>(null)`, derivar
`const busy = action !== null` (mantiene guards de reentrancia y el `disabled` de toda la barra) y
keyear cada label: `action === 'descartar' ? 'Descartando…' : 'Descartar'`. Un `busy` compartido entre
modales distintos → un state por flujo (`savingEdit`/`deleting`).
Caso real FacturaIA: bulk-bars de ingesta (#815) y facturas (#818, 3 botones cambiaban a la vez).
Ver [[css-module-camelcase-turbopack]] para otros gotchas de este mismo repo.
