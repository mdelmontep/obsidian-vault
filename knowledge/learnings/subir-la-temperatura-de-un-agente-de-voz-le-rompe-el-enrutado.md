---
title: subir la temperatura de un agente de voz le rompe el enrutado
date: 2026-08-28
source: centro-elphis
tags: [retell, voz, conversation-flow, llm, prompting]
---
`model_temperature` no gobierna solo **cómo redacta**: en un conversation flow las
condiciones de arista son `cond(prompt)` que **evalúa el mismo LLM con la misma
temperatura**. Subirla para que suene menos robótico afloja también el criterio de "¿se
cumple esta condición?".

Medido en Elphis: de 0,22 a 0,6, **2 de 21 llamadas se quedaron atrapadas** en nodos que
no había tocado (`Consentimiento`, `Recoger datos`) — la condición dejó de dispararse. Y
la naturalidad no mejoró: el guion literal subió (38,1 %). Se revirtió a 0,22.

Regla: la naturalidad se compra en el **texto del prompt**, no en la temperatura. Si tocas
la temperatura de un agente con enrutado por LLM, la medición obligatoria no es cómo
habla, es **cuántas llamadas llegan al final** — y hay que mirar las transiciones de nodo
de las transcripciones, porque el juez de la suite no marca "se quedó atascada".
