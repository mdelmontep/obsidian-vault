---
title: en un conversation flow de retell el nodo end cuelga en silencio
date: 2026-08-27
source: centro-elphis
tags: [retell, voz, conversation-flow]
---
Un nodo `type: end` transiciona y ejecuta `end_call` **sin decir nada**. Ni el
`global_prompt` ni la instrucción del nodo anterior lo hacen hablar: el usuario oye
la línea cortarse justo después de decir "no, nada más". En Elphis pasó semanas
así y lo reportó el cliente como "cuelga sin despedirse".

Los `function` y `extract_dynamic_variables` también son mudos. **Solo los
`conversation` hablan de forma fiable.**

Patrón para una frase garantizada (misma receta que la frase de crisis):
`type: conversation` + `instruction: {type: "static_text", text: "..."}` +
`skip_response_edge` al nodo siguiente. Sale literal, sin pasar por el LLM, y
transiciona sin esperar al usuario.

Ver [[retell-nodo-conversacional-debe-cubrir-explicito-el-caso-no-entendi]].

**Mismo mecanismo en un «te paso con alguien» (Simarro, 1-oct-2026):** un nodo
`conversation` solo evalúa sus edges **después de un turno del usuario**. El agente
decía «te paso» y se quedaba esperando; si el cliente callaba, la llamada acababa
por inactividad sin transferir (2 llamadas reales). Receta: frase en static_text +
`skip_response_edge` al nodo transfer. Ver [[retell-los-batch-tests-ignoran-la-timezone-del-agente]].
