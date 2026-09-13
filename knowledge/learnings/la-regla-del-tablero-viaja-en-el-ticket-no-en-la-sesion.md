---
title: en un build de muchas sesiones, la regla de actualizar el progreso viaja en el ticket
date: 2026-09-13
source: agh-iberica
tags: [harness, planificacion, issues, artifact, multi-sesion]
---
Un build partido en ~20 tickets con `/clear` entre cada uno pierde el progreso: cada sesión arranca sin
saber que existe un tablero. Una regla en memoria o CLAUDE.md llega tarde o no llega.
- **La regla va como ÚLTIMO criterio de aceptación de cada ticket** («tablero actualizado: paso X»), no
  solo en memoria: la sesión que coge el ticket la lee sí o sí.
- **Estados anclados a hechos externos**, no a opinión: en_curso = issue asignado · en_revision = PR abierta
  · hecho = mergeado en main. Criterio «cumple» solo con medición citada.
- **0-100 que no miente**: pasos con peso (90 %) + criterios medidos (10 %), tope 99 hasta que TODO esté
  hecho. El 100 es de UNA fase; el global solo aparece cuando todas tienen spec.
- Datos en la base del artifact (`write_db` con `if_version`), nunca republicando el HTML.
Caso: piloto RRHH de AGH (spec #1691, tickets #1692-#1711). Ver [[agh-iberica]].
