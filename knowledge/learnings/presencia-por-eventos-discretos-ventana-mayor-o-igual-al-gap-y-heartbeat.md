---
title: presencia ("activo ahora") calculada de eventos discretos — la ventana debe ser >= al gap de sesionización
date: 2026-07-25
source: claude-code-session
tags: [telemetria, time-tracking, agency-portal, observabilidad]
metadata:
  type: learning
---

Si la telemetría solo emite en eventos discretos (inicio / prompt / fin de turno / cierre) y hay DOS umbrales sobre el mismo `last_activity_at` en capas distintas, tienen que ser la misma constante:

- `ACTIVITY_GAP_MS` (sesionización, 15 min): decide si el evento siguiente extiende el bloque o abre uno nuevo.
- `ACTIVE_WINDOW_MS` (display, 10 min): decide si se pinta como "activo ahora".

Con la ventana MENOR que el gap queda una franja ciega (10-15 min) donde el bloque sigue abierto y extendiéndose pero la sesión desaparece del panel. Fix: `ACTIVE_WINDOW_MS = ACTIVITY_GAP_MS` (importar la constante, no repetir el número).

Residual que la ventana NO arregla: un turno largo (>gap) no emite nada hasta terminar, así que el trabajo en curso parece inactivo. Eso solo se arregla con un **heartbeat** throttleado (1 evento/60s) que extienda el bloque sin tocar contadores de prompts ni disparar resúmenes — no subiendo la ventana, que además dejaría "activas" las sesiones abandonadas.

Ver [[git-worktree-dotgit-es-fichero-basename-devuelve-la-rama]] · [[merged-duration-intervalos-solapados-time-tracking]]
