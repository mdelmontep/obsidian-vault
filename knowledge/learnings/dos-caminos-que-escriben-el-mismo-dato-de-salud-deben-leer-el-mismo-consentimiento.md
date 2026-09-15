---
title: dos caminos que escriben el mismo dato de salud deben leer el mismo consentimiento
date: 2026-09-14
source: centro-elphis
tags: [rgpd, consentimiento, retell, n8n, voz]
---
Un agente de voz registra el lead dos veces: la tool durante la llamada (con el `si|no` que la persona dio) y el webhook post-call, que relee la transcripción con su propio extractor LLM. El guard de consentimiento solo estaba bien en el primero: el post-call borraba el motivo solo si su extractor marcaba `false` explícito, y "no lo marcó" = guardar.

Caso (`call_328bf40550ab0f62e7828c66155`): la persona dijo «no», la tool quitó el motivo, y 1 min después el post-call escribió motivo + resumen con diagnósticos en el deal, la ficha del contacto y el WhatsApp de aviso.

Patrón:
- El consentimiento es un HECHO capturado en la llamada, no algo a reinferir. Retell lo trae en el webhook `call_analyzed`: `call.collected_dynamic_variables.dv_<variable>`.
- Todo camino que escriba el dato sensible lee ESA variable con la misma regla; el extractor, como mucho, segunda red.
- Si hay resumen libre (`call_summary`), cae con el motivo: repite la sustancia.
- Al auditar un guard de datos sensibles, `grep` de todos los escritores del campo, no solo del que falló.

Relacionado: [[retell-post-call-analysis-persistir-datos-estructurados]] · [[una-obligacion-legal-no-puede-colgar-del-prompt-del-llm]]
