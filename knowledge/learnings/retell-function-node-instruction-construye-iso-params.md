---
title: en retell los args de una tool los gobierna la descripción del parámetro, no la instruction del function node
date: 2026-06-04
updated: 2026-09-28
source: simarro
tags: [retell, conversation-flow, tools, prompting]
---
**Corregido el 28-sep-2026 con medida** (junio decía que la `instruction` del function node construía los ISO). Con Talk While Waiting, la `instruction` es el prompt de la **frase de espera** (docs de Retell):
- Si solo describe args, el LLM rellena la espera inventando el resultado ("hay hueco a las cinco", "queda reservada"). Fix determinista: `speak_during_execution:false` si la tool tarda <1,5 s, o `instruction.type:"static_text"` ("Dame un segundo.").
- Los args salen de la conversación + el **schema de la tool**. Ventana −1h/+2h escrita en la instruction: 10/70 la cumplían; en la `description` de After/Before con ejemplos: 53/70. Mismo patrón con `phone`.
- Las copias `node.tool` embebidas pueden divergir de `tools[]` (Simarro declaraba `_after/_before` con `After/Before` required): igualarlas al parchear.
- Fecha: verbalizar la fecha resuelta en el nodo anterior ("te lo miro para el jueves uno de octubre") ancla el día; sin eso consultó "jueves" como viernes 4/69.
Regla: lo que debe cumplir un argumento → descripción del parámetro con ejemplo; lo que se dice mientras corre → static_text o silencio.
Relacionado: [[retell-from_number-no-auto-sustituye-en-tool-args]] · [[simarro]]
