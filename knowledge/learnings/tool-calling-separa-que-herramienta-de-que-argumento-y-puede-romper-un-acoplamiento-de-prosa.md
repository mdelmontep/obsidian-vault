---
title: migrar de prosa-JSON a tool-calling puede romper un acoplamiento de prompt que parecía sin salida — remide antes de construir la superficie nueva
date: 2026-08-04
source: claude-code-session
tags: [llm, prompt, tool-calling, agh, evals]
---
Caso AGH (#851): con emisión en prosa, 5 redacciones medidas (n=25 entrelazado) mostraban un trade
ACOPLADO sin salida — toda redacción que compraba una capacidad («¿qué tengo en cada cliente?» → la
cartera agregada) costaba un repro real («qué tengo con el cliente Odeon», de 24/25 a 20/25 o peor).
Se dejó sin mergear y documentado como "no hay redacción que no cueste algo".

Tras migrar las lecturas a **tool-calling** (function-calling con schema, #868), la MISMA pregunta —
mismas dos frases, mismo modelo — se remidió: **25/25 en la capacidad y 25/25 intacto el repro**, con
solo una frase añadida a la descripción de la herramienta. Cero acoplamiento.

La causa: en prosa-JSON, «qué herramienta usar» y «qué argumento poner» son la MISMA decisión del
modelo, resuelta en una sola pasada de texto libre — dos reglas compiten por la misma superficie
([[un-prompt-es-una-superficie-con-localidad-no-un-documento]]). Con tool-calling, son DOS decisiones
separadas (qué función invocar, luego qué valor dar a cada argumento nullable) — dejan de competir por
el mismo espacio.

Corolario: un trade de prompt medido como "sin salida" bajo un mecanismo de emisión (prosa-JSON) NO
se hereda automáticamente a otro mecanismo (tool-calling). Si el sistema migra de uno a otro,
remedir ANTES de construir la superficie nueva que el trade parecía justificar — puede que ya no
haga falta.
