---
title: reprocesar contra una rpc idempotente por clave natural es un no-op caro
date: 2026-09-01
source: agency-portal
tags: [batch, llm, idempotencia, postgres]
---
La escritura de veredictos del juez de Flota IA es una RPC idempotente por
`(interaction_id, judge_round)`: si ya hay fila para esa clave, `return` y no
escribe. Perfecto contra reentregas del proveedor — y una trampa al reprocesar.

Reencolar los 182 jobs con **su ronda original** habría enviado los lotes a la
Batch API, pagado, y al recoger la RPC habría cortado en la primera línea: cero
veredictos escritos, cero rastro de error, dinero gastado. La idempotencia no
distingue «esto ya llegó» de «esto quiero rehacerlo».

Regla: **reprocesar exige clave nueva, no reencolar la misma.** Aquí, sufijo
explícito (`m12@1756563720+rejudge1`): la RPC no encuentra previa, supersede la
vigente y escribe. Las otras dos salidas eran peores — borrar las evaluaciones
rompe la inmutabilidad y cascadea las ocurrencias; falsear el epoch +1 s miente
sobre el estado de la conversación.

Cómo se ve venir: leer `prosrc` de la RPC en prod **antes** de mandar el lote.
Ver [[agentesia]] · [[upsert-atomico-rpc-vs-check-then-act-evita-lost-update]]
