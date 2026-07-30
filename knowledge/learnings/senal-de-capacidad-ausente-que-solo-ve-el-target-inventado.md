---
title: una señal de «no sé hacer eso» que solo salta con el target inventado no ve el fallo dominante
date: 2026-07-30
source: claude-code-session
tags: [agentes, llm, observabilidad, evals, agh]
---

Al instrumentar «el agente no supo contestar», el instinto es emitir la señal cuando el modelo
pide una capacidad **que no existe** (target/tool inventado). Medido contra el modelo real: de
9 preguntas fuera de superficie, **cero** llegaron por ahí. 2 pidieron aclaración, 1 escribió, y
**6 rutaron a un target REGISTRADO de verdad** con el filtro que discrimina la pregunta ausente.

O sea que la forma **dominante** del hueco es «contesta otra pregunta con una capacidad válida»:
«¿qué recordatorios tengo puestos?» → devuelve la lista de **tareas**; «¿qué cerré esta semana?»
→ devuelve el pipeline **abierto**. Sin señal, sin error, traza `handled:true`. Es peor que un
«no sé»: el usuario reformula una negativa, pero una lista plausible de la entidad equivocada
se la cree.

Consecuencias: (1) esa clase de fallo **no es observable en producción** con la señal ingenua —
solo se ve con un banco de casos que asierte sobre la INTERPRETACIÓN (target + args), no sobre
el texto; (2) ensanchar la señal a «read sin args» sería ruido hasta que existan descriptores
de campos filtrables, porque muchas lecturas legítimas no llevan args.

Ver [[el-caso-que-mide-un-hueco-entra-antes-que-la-capacidad]] · [[agh-iberica]]
