---
title: el cierre escrito antes de acabar la sesión caduca dentro de su propia PR
date: 2026-08-06
source: claude-code-session
tags: [proceso, documentacion, snapshot, git]
---
Un ritual de cierre que escribe el documento de estado **y luego sigue trabajando** produce un commit
que miente. Caso real: la PR de cierre decía *«seis PRs listas, cero mergeadas — el merge lo bloquea el
harness»*; media hora después el bloqueo se levantó, se mergearon las seis, y esa PR **seguía diciendo
lo contrario** con el gate verde y sin conflicto. Mergearla habría dejado el fichero canónico del
proyecto afirmando algo falso en `main`.

Y ese modo de fallo ya se había pagado en ese repo: un bloqueante descrito como VIVO dos días después
de arreglarse hizo que una sesión lo cogiera como «el siguiente paso obvio». **Un doc de estado
desactualizado es peor que un issue sin cerrar**: quien lo lee no tiene forma de saber que va contra
la realidad.

**El patrón que lo evita:** la PR de cierre es la **última** cosa que se mergea, y justo antes de
mergearla se re-lee **su propio diff** contra lo que ha pasado desde que se escribió. Si la sesión
siguió, el cierre se corrige en un commit encima — no se mergea «porque el gate está verde», que aquí
no mide nada: el gate valida código, no si el texto sigue siendo cierto.

**Señal de alarma concreta:** cualquier frase del cierre en presente sobre algo que aún no ha ocurrido
(«esperando ojo», «cero mergeadas», «pendiente de X»). Son las que caducan primero, y son exactamente
las que la siguiente sesión lee como estado actual.
