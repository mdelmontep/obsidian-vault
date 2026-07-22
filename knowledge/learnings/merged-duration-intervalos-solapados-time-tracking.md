---
title: sumar duración de sesiones concurrentes sin fusionar intervalos duplica el tiempo
date: 2026-07-22
source: claude-code-session
tags: [time-tracking, agregacion, agency-portal]
metadata:
  type: learning
---

Si un mismo actor (persona, worker) puede tener N registros de actividad en paralelo sobre la misma clave de agrupación (mismo proyecto), sumar `duración` de cada fila por separado multiplica el tiempo real por N. Caso: agency-portal `/agency/time` — 3 sesiones de Claude Code abiertas a la vez en el mismo proyecto sumaban 3x la hora real trabajada.

**Fix**: antes de sumar, fusionar los intervalos `[started_at, ended_at ?? last_activity_at]` que se solapan (sort por inicio, merge si `next.start <= current.end`) y sumar la UNIÓN resultante, no cada fila.

**Ojo con el scope de la fusión**: solo fusionar DENTRO del mismo actor — si 2 personas distintas trabajan a la vez en el mismo proyecto, su tiempo SÍ debe sumarse (son 2 horas reales de trabajo, no 1). Agrupar por `(actor, proyecto)` antes de fusionar, nunca fusionar across actores.

Aplica a cualquier feature de time/usage tracking con sesiones potencialmente concurrentes (voice billing, agent runs, etc.), no solo a este caso.
