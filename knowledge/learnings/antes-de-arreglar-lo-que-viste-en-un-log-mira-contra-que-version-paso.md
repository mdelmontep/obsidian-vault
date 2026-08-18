---
title: antes de arreglar lo que viste en una conversación vieja, mira contra qué versión pasó
date: 2026-08-18
source: claude-code-session
tags: [llm, prompt, metodo, debug, elphis]
---
El cliente enseñó una conversación donde el bot preguntaba el motivo que la persona ya le había
dicho. Reflejo: reescribir el prompt. Antes de tocarlo, dos comprobaciones de un minuto:

1. **Fecha del caso vs fecha del último cambio.** La conversación era del 11-ago; la regla que lo
   arregla («REUTILIZA lo que ya sabes, pide SOLO lo que falte») entró el 15. El fallo ya no existía.
2. **Reproducir el turno exacto contra la API real** con el prompt vivo, el mismo historial y el
   mismo modelo: 0/5 repreguntas con el contexto vacío y 0/5 con él poblado.

Sin esto habría reescrito un prompt que ya estaba bien, arriesgando una regresión en lo que sí
funciona, y habría dado por arreglado algo que nunca se midió. En un bot con poco tráfico esto pasa
mucho: **las correcciones se acumulan sin estrenar**, y las quejas siguen llegando de conversaciones
anteriores al fix. Y el corolario: si tu corpus de quejas es viejo, la prioridad no es tocar el
prompt, es **medirlo**.
