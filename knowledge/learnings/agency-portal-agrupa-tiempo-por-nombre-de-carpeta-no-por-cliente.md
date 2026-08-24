---
title: agency-portal agrupa el tiempo trabajado por nombre de carpeta, no por cliente
date: 2026-08-12
source: claude-code-session
tags: [agentesia, agency-portal, time-tracking]
---
`agency-portal` no tiene una lista de clientes en código. Cada sesión de Claude Code se etiqueta con el nombre de la carpeta raíz `.git` donde corrió (o el basename crudo del `cwd` si no hay ningún `.git` subiendo desde ahí) — `resolveProjectName()` en `src/lib/time-tracking/backfill.ts:163`. Ese string se guarda como texto libre en `work_sessions.project`, sin FK a cliente.

Solo se agrupa bajo un cliente si existe fila en `time_tracking_projects` (`supabase/migrations/20260728120000_time_tracking_rates.sql`) vinculando ese `project_key` exacto a un `client_id` — vínculo manual en `/agency/time` → ajustes del proyecto (`project-settings-dialog.tsx`).

Gotchas: (1) no hay alias entre nombres de carpeta distintos — `simarro_web`, `simarro-properties-web` y `simarro` son 3 `project_key` que necesitan su propia fila aunque sean el mismo cliente. (2) si la sesión corre con `cwd` sin bajar a una carpeta con `.git` (ej. desde `~/Projects` raíz), el fallback mete el trabajo en un cubo genérico que mezcla clientes — y eso no se puede reatribuir por UI a posteriori, solo con `UPDATE` directo en `work_sessions`. (3) una carpeta suelta homónima sin `.git` (`~/Projects/elphis` vs `~/Projects/elphis-psicologia`) acumula horas mal atribuidas en silencio durante días — nadie lo nota hasta mirar el gráfico. (4) el mismo `claude_session_id` puede reaparecer días después (sesión retomada) con bloques de trabajo real distinto entremedias: antes de reatribuir, verificar el CONTENIDO de cada bloque (cwd + texto del transcript en esa ventana horaria), no asumir por fecha — caso real: `4cf61623-…` tenía bloques del 22 y del 24-ago, todos Elphis Psicología, confirmado leyendo el transcript.
