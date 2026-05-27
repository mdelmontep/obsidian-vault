---
title: tool conversacional en agente LLM "solo JSON" debe envolver su respuesta en el tipo enrutado
date: 2026-05-27
source: claude-code-session
tags: [n8n, llm, bot, contrato]
---
Si un AI Agent tiene contrato "responde SOLO JSON {tipo,...}" y un nodo downstream parsea por `data.tipo`, añadir tools que devuelven texto natural (cashflow, análisis) ROMPE el parser: el LLM responde el texto crudo → `JSON.parse` falla → el usuario recibe "el agente no devolvió JSON". Per-tool pasa el smoke aislado; la composición revienta.

Fix: instruir en el prompt que la respuesta de esas tools se devuelva envuelta en un tipo que el parser YA enruta, p.ej. `{"tipo":"conversacion","mensaje":"<texto>"}`. NO hace falta tocar el parser si `conversacion` ya va a un responder de texto (verificarlo en el workflow antes).

Además distinguir en el prompt tools de LECTURA (interpretar resultado, sin confirmar) vs ACCIÓN (exigir `ok=true` antes de dar por hecho). Un "exige ok=true" global bloquea las de lectura que no devuelven `ok` (o haz que el endpoint de lectura devuelva `ok:true`).

Caso FacturaIA bot WA Boost v1 (`pqSWkDIHqmSVHotB`). Ver [[extender-tipo-en-agente-json-out-parchear-downstream-o-lookup-recurso]].
