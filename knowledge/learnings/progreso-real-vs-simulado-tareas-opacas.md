---
title: barra de progreso de tarea async opaca — hitos reales backend + estimador monótono cliente, nunca Math.random
date: 2026-06-23
source: claude-code-session
tags: [frontend, react, ux, ocr]
---
Simular progreso con `Math.random` en el cliente parpadea: cada refresh (realtime/poll) reescribe la lista con el progreso real de BD (0) y resetea la barra → salta atrás sin parar.

Patrón correcto:
- Backend emite hitos REALES en los puntos genuinos del pipeline (OCR: 20 al despachar a la IA, 65 al responder, 100 al terminar), con guard `estado=procesando` para no revertir el estado final.
- Cliente refleja de forma MONÓTONA: merge `max(progresoBD, progresoLocal)` (nunca retrocede) + estimador por tiempo real `1−e^(−t/τ)` para el único tramo opaco, saturando por debajo del siguiente hito.
- Refresh de fondo silencioso (no togglear loading ni vaciar la lista en error transitorio) + debounce del realtime (coalesce ráfagas) + ref a la última callback para evitar closure stale al cambiar de página.
- Probar la invariante con tests: el merge nunca decrece bajo refreshes adversos (server→0, fuera de orden).
Hermano del parpadeo por filtros inline object → render loop (incident 2026-06-21 #439).
- **Optimistic insert al subir**: sin él, el skeleton espera el evento realtime (~500ms). Insertar el item localmente al recibir el `id` del upload (`estado:'procesando', progreso:0`) y auto-seleccionarlo da visibilidad inmediata. Guard: `prev.some(b => b.id === id)` para no duplicar cuando llega realtime.
