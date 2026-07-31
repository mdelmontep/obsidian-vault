---
title: un guard colgado de un flag calculado una vez solo cubre el mundo de ese instante
date: 2026-07-31
source: claude-code-session
tags: [guards, deteccion, datos, verificacion]
---
Un guard que exige confirmación al aprobar un posible duplicado quedó correcto y bien colocado
(en la transición única, cubriendo web, lote, API y agente)... y **casi nunca se dispara**.

La causa: leía `review_reasons`, un flag que el OCR calcula **una sola vez al ingerir**. Si la
factura con la que choca entra DESPUÉS, el documento ya ingerido no vuelve a evaluarse y nunca
recibe el flag. Medido en producción: **1 fila con el flag frente a 13 grupos de duplicados
reales**. El guard cubría 1 de 14.

Regla: antes de colgar un guard de un flag, pregunta **cuándo se calculó y qué ha cambiado
desde entonces**. Si la condición depende de otras filas, consúltalas en el momento de decidir
en vez de fiarte de una foto vieja — muchas veces esa consulta ya la haces para construir el
mensaje de error, y basta con invertir el orden.

Corolario incómodo: cerrar el issue con el guard puesto hace creer que el caso está cubierto.
Una marca sin dientes se cambia por un guard sin datos. Caso real: FacturaIA `qa-022` → `qa-030`.

**Resuelto 2026-07-31 (`qa-030`)**, y el criterio del arreglo importa tanto como el arreglo: al
consultar en vivo hay que decidir **qué filas cuentan**. Aquí solo las que ya están en los libros
(`NOT IN ('sin_aprobar','disputada')`). Si contase la gemela todavía sin aprobar, la PRIMERA de un
par recién subido pediría confirmación sin motivo; excluyéndola, la primera pasa y la segunda choca
con la que ya entró, que es exactamente el incidente que se quería evitar.

Dos efectos colaterales que hay que cubrir en el mismo PR: la consulta pasa de informativa a
decisoria, así que tiene que distinguir "no hay colisiones" de "no he podido mirar"; y el aviso pasa
de saltar 1 vez de 14 a saltar siempre que toca, así que **todas** las pantallas que reciben ese
error necesitan salida (una de ellas solo tenía un toast genérico: habría sido un callejón sin salida).

