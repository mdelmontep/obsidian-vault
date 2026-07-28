---
title: estar en el catálogo de crons no es estar programado, y el que nunca corrió parece sano
date: 2026-07-28
source: claude-code-session
tags: [monitoring, cron, alerting, facturaia, metodo]
---
Con el catálogo en código (`CRON_REGISTRY`) y el scheduler fuera (Dokploy), añadir
la entrada y olvidar el `schedule.create` deja un cron que **no existe** y nadie lo
nota: sin runs, la salud sale `'desconocido'`, y el colector de incidencias solo
mira `'rojo'`. Silencio leído como salud. En TuFacturaIA
`obras-reservas-reconciliar` — la red de seguridad de las reservas de obra —
llevaba desde su despliegue sin ejecutarse ni una vez.

Fix: tratar "cero runs" como incidencia propia (`cron_nunca_ejecutado`), severidad
ALTA aunque el cron sea housekeeping (no hay nada programado que se recupere solo)
y que se resuelve sola en el primer run, así que no puede quedarse sonando.
La dirección contraria (corriendo sin entrada en el catálogo → invisible en el
panel) no la detecta nada automático: hay que diffear el catálogo contra
`schedule.list` de vez en cuando.

Lo que más escuece: el hueco **ya estaba documentado** en `gotchas.md` con un
"auditar de vez en cuando", y mordió igual. Un recordatorio en la documentación no
es un mecanismo — si el fallo es silencioso, la única defensa es código que grite.

Ver [[cron-mantenimiento-auto-sanable-no-debe-paginar-severidad-por-criticidad]] ·
[[dependabot-no-avisa-de-eol-de-runtime]]
