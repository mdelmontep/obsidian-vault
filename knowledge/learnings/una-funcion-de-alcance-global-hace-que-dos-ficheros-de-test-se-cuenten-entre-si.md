---
title: una función de alcance global hace que dos ficheros de test se cuenten entre sí
date: 2026-09-05
source: mandadm
tags: [testing, vitest, postgres, concurrencia, metodo]
---
`notifyPendingAlerts` barre **todas** las alertas pendientes de la instalación. En producción es
correcto —es lo que debe hacer un cron—, pero vitest corre los ficheros **en paralelo contra el mismo
Postgres**, así que dos ficheros que insertan alertas pendientes se ven las filas del otro. Son dos
fallos distintos y **solo uno se arregla igual**:

- **Contar de más** — `toHaveLength(1)` sobre todo lo enviado. Se acota la aserción a un dato **único**
  del test (el texto del detalle), nunca al `kind`, que los dos comparten.
- **Que te muten las filas** — el barrido ajeno marca TUS alertas como notificadas antes de que
  compruebes. Acotar no lo arregla: hace falta **exclusión mutua**. `pg_advisory_lock(<clave>)` en un
  `beforeEach` registrado el **primero** (corren en orden de registro) y `pg_advisory_unlock` en el
  `afterEach` (corren en orden **inverso**), sobre una conexión propia.

El cerrojo hay que **probarlo**, o es una línea inerte que da sensación de arreglo: otro cliente hace
`pg_try_advisory_lock` de la misma clave y tiene que devolver `false` mientras lo tienes.

Y no apagues el paralelismo: el cerrojo cuesta dos ficheros, `--no-file-parallelism` cuesta la suite.
Ver [[el-agotamiento-de-un-pool-se-disfraza-de-lentitud-no-de-error]] · [[test-verde-puede-codificar-el-bug-como-esperado]]
