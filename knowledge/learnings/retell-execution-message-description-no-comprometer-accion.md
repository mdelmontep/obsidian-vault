---
title: retell execution_message_description no debe comprometer la acción futura
date: 2026-05-25
source: simarro
tags: [retell, voice, tools, prompt-engineering]
---

`execution_message_description` es lo que Retell le pide al LLM que diga **mientras la tool se ejecuta**, para cubrir el silencio del HTTP. Dos formas de romperse, las dos medidas en producción:

1. **Compromete una acción que aún no se ha decidido.** Con "Dile que estás registrando la llamada para derivarla a la persona adecuada", Laura (Tecnocloud) lo verbalizaba en el primer turno y disparaba la tool antes de preguntar el motivo.
2. **El modelo suelta ahí la respuesta entera y la repite al volver.** Simarro, 9-sep-2026 (`call_924981bcc…`): con la descripción neutra "A ver qué tenemos", Ana contestó la regla de negocio completa mientras corría la función (60,7 s) y el nodo destino se la hizo repetir al volver (74,1 s). El cliente lo oye como tartamudeo del bot.

Regla: descripción **neutra** ("dame un segundo que lo miro"), sin prometer nada; y en el `global_prompt`, una línea explícita de que mientras corre una función solo se dicen frases de espera — nada de cifras, condiciones ni compromisos — y que si ya se dijo, al volver **no se repite**.

La causa raíz del caso 2 suele ser una transición sobrante: revisa antes si el edge que llevó a la función estaba de más ([[un-edge-abierto-manda-a-buscar-lo-que-ya-estaba-en-pantalla]]).
