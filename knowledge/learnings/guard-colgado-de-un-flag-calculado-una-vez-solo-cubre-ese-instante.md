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
