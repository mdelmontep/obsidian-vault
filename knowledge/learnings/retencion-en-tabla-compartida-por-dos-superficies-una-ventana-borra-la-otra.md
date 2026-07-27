---
title: un cron de retención sobre una tabla que sirve a dos superficies necesita una ventana por superficie
date: 2026-07-25
source: claude-code-session
tags: [retencion, crons, privacidad, postgrest, facturaia]
---

**Patrón**: se añade retención corta para una superficie (historial web del Copiloto, 2 h con el flag apagado) y el cron filtra solo por org. Pero esas tablas también guardan los hilos de **WhatsApp** y los **proactivos**, así que la ventana de 2 h les caía encima y les partía la conversación al usuario de un día para otro, anulando la ventana de 30 días decidida para el canal.

**Fix**: una pasada por superficie, con su propio `cutoff`. Discriminador `titulo` (`'WhatsApp'`/`'Sistema'` los fuerza el código en esa población, así que es fiable). Dos trampas al filtrar el negativo en PostgREST:
- `NOT IN` con `NULL` da `NULL` y **descarta** la fila → el hilo sin título no se podaría nunca. Hay que contemplarlo: `.or('titulo.is.null,titulo.not.in.(…)', { referencedTable })`.
- No filtrar el lado web por igualdad con el título neutro: una org que tuvo el flag ENCENDIDO conserva hilos con la pregunta como título, y también hay que podarlos.

**Cómo se cazó**: al ir a dar de alta el schedule, no al escribirlo. El cron no había corrido nunca, así que no hubo pérdida. Antes del primer run se midió en seco contra prod cuántas filas borraría (0: nadie tenía el flag apagado) — un cron de borrado no se estrena a ciegas.

Ver [[tablas-de-log-sin-retencion-dominan-el-tamano-de-la-bd]] · [[fk-cascade-desde-tabla-de-auditoria-la-poda-borra-la-prueba]].
