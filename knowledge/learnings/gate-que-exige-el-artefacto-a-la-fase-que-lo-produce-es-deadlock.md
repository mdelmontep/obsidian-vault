---
title: gate que exige el artefacto a la fase que lo produce es un deadlock
date: 2026-08-21
source: facturaia
tags: [pipelines, gates, testing, agentes]
---
Un gate «no sirvas X sin el artefacto Y aprobado» aplicado a TODO llamador
bloquea también a la fase cuyo trabajo es ESCRIBIR Y: desde ese momento ningún
elemento nuevo puede estrenar el artefacto y el pipeline entero se seca.
Caso real (facturaia contenido-25): los contextos de producción exigían plan
aprobado a todo el mundo, incluido el planificador que venía a escribirlo →
ninguna pieza estrenó plan durante semanas y los runs nocturnos morían con
`plan_no_aprobado`.
La suite no lo vio porque el test del planificador MOCKEABA el contrato que
imponía el gate: el mock cumple lo que el servidor real niega.
Fix: el endpoint distingue la fase productora (`fase=plan` sirve sin exigir el
plan y sin devolverlo; fase desconocida → 400) y los consumidores siguen con el
gate intacto. Al testear pipelines con gates: al menos un test integra el gate
real contra la fase productora, no solo mocks por fase.
