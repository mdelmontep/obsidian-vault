---
title: un FOR UPDATE que no encuentra fila no bloquea nada, y el subquery del FROM no se re-evalúa
date: 2026-08-13
source: claude-code-session agh-iberica
tags: [postgres, concurrencia, race-conditions, audit, upsert]
---
Dos gotchas de Postgres que se combinan y rompen el mismo invariante: **saber qué había justo antes**
de una escritura. Medidos con dos sesiones interleaveadas, no deducidos.

**1. `SELECT … FOR UPDATE` sobre una fila que NO existe no toma ningún candado.** No hay fila que
bloquear y Postgres no bloquea el hueco. Así que el patrón «pre-read para el `before` + upsert» cierra
la carrera de **actualización** y deja abierta la de **creación**: dos primeras escrituras concurrentes
leen las dos `null` y auditan las dos `create`. El valor final es correcto (gana el último); lo que se
pierde es la transición. Y no se ve en tests: con fila existente sí bloquea, así que el caso normal
pasa. **Quien resuelve esa carrera es el `INSERT … ON CONFLICT DO NOTHING`** — el índice único hace
esperar al segundo hasta que el primero confirma. Si devuelve fila, la creaste tú (`before = null`); si
no, ya existe y **ahora sí** hay fila que bloquear.

**2. `UPDATE … FROM (SELECT …) prev` NO re-evalúa el subquery bajo EPQ.** Bajo READ COMMITTED, un
`UPDATE` que espera a otra transacción re-evalúa su `WHERE` con la fila nueva — pero el subquery del
`FROM` se quedó con el snapshot viejo. Medido: sin `FOR UPDATE` dentro del subselect, el segundo lee
`before=v0` en vez de `vA`. **Con** `FOR UPDATE` dentro, sale el bueno.

**Patrón que cierra las dos**, y en dos sentencias atómicas por sí solas (no hace falta que el llamante
recuerde envolver en transacción): `INSERT … ON CONFLICT DO NOTHING RETURNING …` y, si no creó,
`UPDATE … FROM (SELECT … FOR UPDATE) prev … RETURNING prev.value, u.value`. Trae `updated_at` del
subselect también, o el «anterior» llevará el sello de la escritura nueva.

⚠️ Descartado `RETURNING (xmax = 0)`: dice si insertó, pero **no da el `before`**. Media solución.
Y ojo al medir: el `FOR UPDATE` del punto 2 puede salir como mutante **equivalente** porque el INSERT
de arriba ya absorbió la espera — protección vecina, ver
[[verificar-que-un-test-tiene-dientes-con-una-mutacion]].

Caso real: AGH #1042. Corrige a [[audit-log-multi-escritor-procedencia-en-after-before-sin-carrera]].
