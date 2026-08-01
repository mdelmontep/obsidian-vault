---
title: filtrar por call_successful en la api de retell devuelve 500
date: 2026-08-01
source: claude-code-session
tags: [retell, api, gotcha]
---
`POST /v2/list-calls` con `filter_criteria: { agent_id: [...], call_successful: [true] }`
responde **500 Internal Server Error**, sin mensaje útil. Con sólo `agent_id` funciona.

Fix: pedir un lote amplio (`limit: 200`) filtrando únicamente por agente, y descartar en
cliente por `call_analysis.call_successful`, `duration_ms` y `recording_url`.

Y para elegir un fragmento publicable no basta con la métrica: hay que **leer la
transcripción**. Las llamadas mejor puntuadas arrancaban con silencios largos («¿sigues
ahí?») o con el cliente repitiéndose, que en una demo de 30 s se nota más que en la
llamada entera. Ver [[los-audios-de-llamadas-reales-llevan-nombres-de-clientes]]
