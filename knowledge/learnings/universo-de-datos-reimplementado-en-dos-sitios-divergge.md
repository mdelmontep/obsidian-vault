---
title: si dos sitios reimplementan el mismo universo de datos, divergen y el diff miente
date: 2026-07-26
source: claude-code-session
tags: [arquitectura, cron, deteccion-de-cambios, supabase]
---

Un detector de cambios (cron de deriva, sync, invalidación de caché) compara "lo
que hay ahora" contra "lo que se guardó". Si el conjunto de "lo que hay ahora" se
calcula con una query PROPIA en vez de leerlo de la misma fuente que lo guardó,
las dos copias divergen y el diff empieza a mentir.

Caso real (FacturaIA, cron `fiscal-recalcular-borrador`): el snapshot del modelo
303 guardaba emitidas Y recibidas; el diff del cron consultaba solo
`tipo='emitida'`. Cada recibida salía como "saliente" → `requires_recalc` y
cuadres BORRADOS cada noche en 3 declaraciones, 5 noches con el mismo número.
El cron también recalculaba el rango de fechas con su propio mapa de trimestres
en vez del helper: misma clase de bug, latente.

Dos agravantes que multiplican el daño:

- **Deduplicación de avisos**: el aviso iba con índice único
  `(declaracion_id, tipo)`. El falso positivo quemó el único hueco, así que una
  deriva REAL posterior no habría notificado nunca. Un falso positivo sobre un
  canal deduplicado no es ruido, es pérdida de señal.
- **Falso positivo por el otro lado**: al mirarlo, las filas que el motor carga
  pero NO clasifica tampoco llegan al snapshot, así que incluirlas en el universo
  las habría marcado como "nuevas" para siempre.

Fix: extraer el universo (tipos, rango, filtros) a un módulo único que consuman
el productor y el detector. Y una regresión que se verifique EN ROJO: un test de
"snapshot = live → sin cambios" es el que caza esto; el de "hay cambios → avisa"
pasa igual con el bug dentro.
