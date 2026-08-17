---
title: order by created_at empata dentro de la misma transacción y la aserción de orden es una lotería
date: 2026-08-17
source: claude-code-session
tags: [postgres, testing, flakiness, sql]
---

Un test que escribe N filas **en la misma transacción** y luego las lee con `ORDER BY created_at`
está aseverando un orden **que la consulta no define**: `now()`/`CURRENT_TIMESTAMP` es el timestamp
**de transacción**, así que las N filas comparten `created_at` al microsegundo y el orden que devuelve
Postgres depende del plan y del orden físico de las filas.

Sale verde casi siempre, y por eso se lee como flake del entorno cuando aparece.

- **Lo que cambia el resultado es la BASE, no el diff**: en una base con datos y páginas ya escritas
  el orden físico sale estable; en una **recién migrada**, no. Medido: `main`/`agh_dev` 9 passed ×2 ·
  rama/`agh_dev` 9 passed ×2 · rama/base efímera **1 failed**. Así que cuando el gate pasa a crear su
  base de cero en cada corrida, este empate **empieza a salir más, no menos**.
- **Contrafáctico correcto**: misma rama y misma base, no «rama contra main» — comparar en bloques
  mide la hora.
- **Fix**: desempatar en la consulta (`ORDER BY created_at, id`), **no** relajar la aserción a
  conjunto: si se compara como conjunto se pierde la propiedad «el audit de A va antes que el de B»,
  que suele ser justo lo que el test dice verificar.
