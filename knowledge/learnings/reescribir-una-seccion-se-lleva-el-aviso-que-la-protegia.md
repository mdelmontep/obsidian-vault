---
title: reescribir una sección se lleva por delante el aviso que la protegía
date: 2026-09-05
source: facturaia — gate de cierre, ticket de soporte 171
tags: [documentacion, runbooks, gate, gotcha]
---

Un runbook acumula avisos pegados al paso que protegen («esto pisa el campo», «esto
no es reversible»). Al reescribir ese paso, el aviso se va con él **y el paso
peligroso sigue en otra sección**, ahora desnudo. El diff se ve limpio: son líneas
borradas de algo que se reescribió.

Caso real: la reescritura de la fase 1 de un plan borró el comentario «el PATCH
reemplaza el campo» de `notas_internas`; la fase 7, intacta, seguía mandando escribir
ahí. Quien lo siguiera destruía el histórico interno del ticket, incluido el registro
de un falso cierre. Lo cazó el gate de cierre, no una lectura.

Regla: al reescribir un paso de un runbook, `grep` del identificador que tocaba
(`notas_internas`, el nombre de la tabla, el flag) en el fichero ENTERO, y comprobar
que cada sitio que aún lo menciona conserva su aviso. El aviso vive con el
identificador, no con la sección.

Por eso el gate de cierre corre también sobre diffs de solo documentación: un `.md`
que manda escribir en producción es código. Ver [[una-lista-de-hallazgos-caduca]].
