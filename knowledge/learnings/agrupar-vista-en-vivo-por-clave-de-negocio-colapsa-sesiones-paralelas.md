---
title: agrupar una vista "en vivo" por clave de negocio (no por id único) colapsa sesiones paralelas
date: 2026-07-22
source: claude-code-session
tags: [time-tracking, agregacion, agency-portal, ui]
metadata:
  type: learning
---

Al construir una vista "quién está trabajando ahora" (o cualquier live-status por actor), agrupar por `(actor, proyecto/entidad)` en vez de por el ID único de la sesión colapsa en una sola fila varias sesiones REALES en paralelo que comparten esa clave — el usuario solo ve la más reciente, las demás desaparecen sin rastro.

**Caso real 2026-07-22 (agency-portal, `/agency/time` "Trabajando ahora")**: `buildActiveTree` agrupaba por `(member, project)`; 2 sesiones de Claude Code abiertas a la vez en el mismo proyecto (FacturaIA) se fusionaban en una fila, mostrando solo la síntesis de la sesión más reciente.

**Fix**: agrupar por el identificador único real (`claudeSessionId`), no por la clave de negocio. La clave de negocio (proyecto) sigue sirviendo para fusionar duración de bloques de la MISMA sesión rotada — pero nunca para decidir cuántas filas mostrar.

Distinto de [[merged-duration-intervalos-solapados-time-tracking]] (ese es sobre NO duplicar duración al sumar); este es sobre NO perder filas al mostrar. Ambos bugs conviven en el mismo agrupador si no se separa "clave para fusionar tiempo" de "clave para decidir cuántas entidades distintas hay".
