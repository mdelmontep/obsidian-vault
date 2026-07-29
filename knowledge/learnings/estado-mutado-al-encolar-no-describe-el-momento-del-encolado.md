---
title: el consumidor de una cola no puede leer del estado el motivo por el que se encoló
date: 2026-07-29
source: claude-code-session
tags: [colas, workers, prompts, facturaia]
---

Si encolar cambia el estado de la entidad, el worker que reclama el job segundos después
ya no ve el estado que motivó el encolado: lee el que dejó el propio encolado.

Caso TuFacturaIA: relanzar Claude sobre un ticket `resuelto` lo pone en `en_revision` al
encolar. El claim del runner construía el prompt con `retry: { estado: ticket.estado }` y
para entonces siempre era `en_revision`, así que el bloque "REAPERTURA — el arreglo anterior
no cerró el caso" no salía nunca salvo que hubiera un PR previo que delatara el reintento.

Dos salidas: (a) persistir el dato en la fila del job al encolar (`estado_previo`), que
exige migración; (b) derivarlo de un hecho que el encolado no pisa. Se eligió (b): existe
job anterior (`getIntentoPrevio` → `{ hubo, prUrl }`), con `hubo` separado del PR porque un
intento en `sin_cambios`/`fallido` no deja PR y aun así es un reintento.

Regla: lo que el worker necesita saber sobre "por qué estoy aquí" viaja EN el job o se
deriva de algo inmutable. Nunca de una columna que el propio enqueue acaba de escribir.
