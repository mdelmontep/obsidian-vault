---
title: atribución de "quién usa X ahora" en columna escalar pierde bajo uso concurrente
date: 2026-08-04
source: claude-code-session
tags: [modelado-datos, concurrencia, agency-portal]
metadata:
  type: learning
---

Cualquier feature de "quién está usando este recurso compartido ahora" (cuenta compartida, sesión, lock blando, credencial rotativa) modelada como columnas escalares (`used_by`, `used_by_at`) sobre la fila del recurso solo guarda UN valor. Si dos actores lo usan a la vez, cada reporte SOBRESCRIBE al anterior — no hay error, no hay excepción, solo un dato que miente por omisión (muestra al último que reportó, no a todos).

Caso real: agency-portal, badge "en uso ahora" para una cuenta de Claude Code compartida por el equipo. `member_rate_limits.used_by_member`/`used_by_at` (PR #206) parecía correcto y pasó todos los tests — porque nadie probó el caso de dos personas a la vez. Se detectó preguntando explícitamente "¿y si son 2 los que están usando la cuenta?", no por un fallo en producción.

**Fix**: tabla aparte con PK compuesta `(recurso, reportero)` — una fila por reportero, cada uno con su propio timestamp. El lector filtra por ventana de actividad y lista TODOS los que siguen dentro, no solo el último.

**Señal para detectarlo en review/diseño propio**: si un `upsert`/`update` de "quién hizo esto último" tiene como `onConflict` solo la clave del recurso (no `(recurso, actor)`), es last-writer-wins y no soporta concurrencia — preguntarse explícitamente "¿puede haber más de un actor a la vez aquí?" antes de dar el diseño por cerrado.
