---
title: agrupar por hash de la prosa de un LLM no agrupa nada
date: 2026-09-01
source: agency-portal
tags: [llm, dedup, taxonomia]
---
La clave de deduplicación de los hallazgos era `categoría:sha256(pattern)`, y el
`pattern` lo redactaba el LLM. Primera corrida real: **134 hallazgos, 131 títulos
distintos, 133 con `occurrence_count = 1`**. No agrupaba nada, y el proposer de
la fase siguiente (exige 3 ocurrencias) no habría disparado jamás.

Causa: cada conversación se juzga aislada, así que pedirle al modelo que el
`pattern` salga «idéntico» en otra conversación es imposible por construcción.

Fix: **agrupar y describir son campos distintos.** El modelo emite un
`patternCode` de una lista CERRADA por categoría (derivada de los 134 títulos
reales) y la clave pasa a `categoría:código` en claro; el `pattern` sigue siendo
prosa y sigue yendo al título. La validación exige que el código pertenezca a su
categoría: uno inventado es fallo con motivo, **nunca se corrige a `other` en
silencio**. Y `other` cae al hash, no a una clave común: duplicar cuesta un clic,
FUNDIR esconde un problema bajo otro ya descartado.

Ver [[agentesia]] · [[dedup-1password-por-titulo-mas-usuario-no-solo-titulo]]
