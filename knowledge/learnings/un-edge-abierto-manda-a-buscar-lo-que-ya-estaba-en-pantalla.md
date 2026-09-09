---
title: un edge abierto manda a buscar lo que ya estaba en pantalla
date: 2026-09-09
source: simarro
tags: [retell, conversation-flow, voice, prompt-engineering]
---

En un conversation flow, el nodo que presenta resultados suele tener un edge del tipo "el cliente pide MÁS opciones, OTRAS o alternativas" hacia el nodo de búsqueda. Ese texto se traga peticiones que **no son** de opciones nuevas: en Simarro (9-sep-2026), "¿podría ver los dos?" — hablando de las dos viviendas ya presentadas — disparó otra `Buscar_viviendas`, esta vez por `idealista_id` de una que ya estaba cargada.

Consecuencias en cadena: coste y latencia de una tool inútil, y sobre todo la respuesta dicha **dos veces**, una mientras corre la función y otra al volver al nodo ([[retell-execution-message-description-no-comprometer-accion]]).

Regla al redactar edges de un nodo de presentación: la condición debe excluir explícitamente **actuar sobre lo ya presentado** (verlo, visitarlo, compararlo, pedir detalles), y el propio nodo debe listar esos casos en su bloque de "responde aquí SIN transitar". Un edge se escribe diciendo también a qué NO dispara; con solo lo que sí, el LLM lo estira.

Se ve en la traza: `transcript_with_tool_calls` trae los `node_transition` con `former_node_name`/`new_node_name` y segundo exacto — el bucle A→B→A en 13 s es la firma.
