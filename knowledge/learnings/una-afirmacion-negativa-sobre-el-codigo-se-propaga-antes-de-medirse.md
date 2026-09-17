---
title: una afirmación negativa sobre el código se propaga a N superficies antes de medirse
date: 2026-09-17
source: agh-iberica
tags: [metodo, evidencia, documentacion]
---
«X no se persiste», «no hay columna para Y», «el tope no existe» se escriben con la
confianza de un hecho y se copian a todas las superficies del cierre: artifact, nota de
sesión, Slack, comentario del issue. Medido el 17-sep: «la propuesta no se persiste» acabó
en CUATRO sitios y era falsa — `text-worker.ts:478` inserta en `hr_field_proposals` en
transacción. El hueco real era otro (el estado de decisión), así que el issue apuntaba a
lo que no era.

Asimetría que lo hace caro: una afirmación POSITIVA la desmiente el primer que la usa; una
negativa nadie la prueba, porque «no está» no se ejecuta. Y **la nota de sesión es
write-once**: de las cuatro superficies, una no se puede corregir nunca.

Regla: antes de escribir que algo NO existe, el `grep`/`sed` del fichero que lo
implementaría, citando línea. Si no se puede citar, va como «no lo he encontrado», no como
«no existe». Ver [[una-revision-con-contexto-limpio-corrige-lo-que-ya-publicaste]].
