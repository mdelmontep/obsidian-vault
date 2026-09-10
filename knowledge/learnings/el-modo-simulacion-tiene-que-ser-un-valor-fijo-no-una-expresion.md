---
title: el modo simulación tiene que ser un valor fijo, no una expresión
date: 2026-09-09
source: simarro
tags: [n8n, dry-run, fail-closed, simarro]
---
Estreno del sync de agentes: lo lancé "en simulación" y **escribió en real**, con un plan de dar de
alta las 6 agendas. Dos bugs independientes, cada uno bastaba:

1. El Set node `dry` con `type: boolean` y **valor por expresión** no evalúa: se queda en `false`
   —justo el valor peligroso—, sin error.
2. PostgREST devuelve **un item de n8n por fila**, así que `$('Leer agentes').first().json` hacía ver
   la tabla vacía y todo parecía un alta. Se lee con `.all().map(i => i.json)`.

Lo que impidió el daño **no fue el código**: fue la constraint `unique` de `agent_key`, que tumbó el
INSERT entero. Verificado a posteriori que la tabla seguía con sus 8 filas.

Reglas: el interruptor de simulación es un **valor literal** (o dos caminos de entrada distintos, uno
por modo), nunca una expresión que pueda no evaluar; y el estreno de un sync se hace contra un
destino con constraints que sepan decir que no. Ver [[un-flag-de-dry-run-que-el-reenviador-ignora-convierte-el-smoke-en-produccion]] · [[una-tabla-que-alimenta-un-matcher-debe-generarse-con-la-normalizacion-del-matcher]]
