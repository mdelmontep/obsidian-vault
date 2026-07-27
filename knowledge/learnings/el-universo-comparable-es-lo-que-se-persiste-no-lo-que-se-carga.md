---
title: el universo comparable es lo que se persiste, no lo que el motor carga
date: 2026-07-27
source: claude-code-session
tags: [fiscal, facturaia, crons, deteccion-de-deriva, refactor]
---

Al unificar en una fuente única el "universo de datos" que dos piezas comparan
(un motor que calcula y un detector de deriva que difiere contra un snapshot),
el conjunto correcto es **lo que la primera pieza PERSISTE**, no todo lo que
carga para calcular. Si el motor lee más de lo que guarda, el diff verá lo no
guardado como novedad cada vez que corra.

Caso TuFacturaIA 2026-07-26/27. El arreglo de [[universo-de-datos-reimplementado-en-dos-sitios-divergge]]
puso emitidas + recibidas en `universoDeclaracion()` para el 303 **y para el
130**. Pero el 130 carga los gastos para las casillas y solo guarda las emitidas
en snapshot (`calculadores/v1/130.ts:308-309`). Resultado la primera noche tras
el despliegue: todas las recibidas del ejercicio salieron como "nuevas" (264
sobre 271 en una org; 6 declaraciones de 3 orgs), el cron marcó
`requires_recalc`, borró los cuadres y quemó el hueco de aviso. El mismo bug que
el refactor cerraba, en dirección contraria — y antes del refactor el cron
acertaba por casualidad, porque miraba solo `tipo='emitida'`.

Con la misma raíz, una segunda comprobación nueva quedó imposible de satisfacer:
el recheck de "marcar presentada" exigía toda recibida viva en el snapshot, así
que un 130 con un gasto aprobado no se podía presentar, sin salida (recalcular y
reabrir dejan el snapshot igual).

Reglas que quedan:

- Al escribir la fuente única, nombrar explícitamente qué es el universo
  ("comparable contra el snapshot") y por qué difiere de lo que se carga.
- Un guard que compara vivo-contra-persistido debe preguntarle al propio
  persistido qué representa (`¿hay filas de este tipo en el snapshot?`), no
  llevar una lista de modelos en SQL: esa lista es la segunda copia del universo
  y volverá a divergir.
- Un modelo con snapshot **parcial** no lo cubre el guard de "snapshot vacío".
  Vacío y parcial son casos distintos.
- El test que cierra esto es el caso mixto (un tipo persistido y otro no), no el
  caso limpio. El test verde que había solo usaba emitidas.

Ver [[fiscal-declaracion-snapshot-es-la-fuente-del-diff]] · [[universo-de-datos-reimplementado-en-dos-sitios-divergge]]
