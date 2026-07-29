---
title: un puntero durable a una fila borrada convierte un fallo puntual en bucle permanente
date: 2026-07-29
source: claude-code-session
tags: [postgres, foreign-keys, estado-conversacional, agentes]
---
Patrón: un estado durable guarda un puntero a otra tabla (`last_client_id`, `last_write`, «lo último mencionado»). El turno que **borra esa fila** lee el puntero al empezar, ejecuta el borrado —la FK `ON DELETE SET NULL` limpia bien— y luego **persiste la variable en memoria**, que aún trae el id muerto → `23503`.

Lo que lo vuelve grave no es el error, es lo que hay detrás: si el catch de ese fallo responde «hecho» y **no limpia el pending**, y la operación es idempotente (un borrado que siempre devuelve `executed`), el usuario entra en bucle. Y **no caduca**: cada turno reescribe `updated_at`, así que el TTL nunca vence mientras siga escribiendo. Caso real: 14 minutos de usuaria atrapada, y seguía atrapada al encontrarlo.

Dos capas, siempre las dos:
1. **Causa** — al ejecutar un borrado, anular los punteros que apunten a la fila borrada, DESPUÉS de sellarlos (el propio payload del borrado suele acabar de sellar el id muerto). En una fusión, RE-APUNTAR al superviviente en vez de anular: la entidad sigue existiendo.
2. **Cinturón** — si la escritura de estado falla, reintentar SIN punteros. Que el pending muera es lo único imprescindible; perder anáfora un turno es barato comparado con un bloqueo.

Solo se reproduce contra la BD real: con un store en memoria no hay FK, así que el bug es invisible por construcción → el test tiene que ser `*.pg.test.ts`.

Caso real: agh-iberica #643. Ver [[guard-en-codigo-que-predice-un-indice-unico-de-sql-diverge]].
