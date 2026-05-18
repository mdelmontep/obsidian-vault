---
title: slot resolver determinista pre-LLM con NLU regex en español
date: 2026-05-18
source: claude-code-session
tags: [bot, llm, nlu, n8n, patron]
---

Bots conversacionales con listas ("cuál convierto?") no deben dejar al LLM resolver "el N" → `items[N-1].id`. Es no-determinista y produce alucinaciones de UUIDs.

Patrón Stripe/Notion/Linear: backend resuelve el slot ANTES del LLM con regex sobre el chatInput. 8 patrones en precedencia explícita (cross-bot):

1. NUM explícito: `P2026-0018`, `0018`
2. Superlativo: "más caro/grande" → max; "más barato/pequeño" → min
3. Fecha: "del 18 de mayo", "del 18-may", "hoy", "ayer", "del 10/05"
4. Importe: "de 289", "289 euros", "4.827,90 €" (tolerancia entero→decimal)
5. Cliente (listado mixto): "el de Borja"
6. Número de slot: "el 1", "#3", "n° 4"
7. Ordinal: "primero..quinto", "último/última"
8. Pronombre / 1-item shortcut: "ese", "el de antes"

Inyecta `resolved_slot: {id, num, ...}` en el state. El LLM lo recibe explícito en `<previous_state>` y la tool lo lee directo. Eliminamos `$fromAI` (que tiene bug en toolCode langchain).

Ver [[$fromAI-en-toolCode-lanza-no-execution-data-available-en-n8n-2.15.x]] · [[ADR-003-slot-resolver-determinista]]
