---
title: una regla de prioridad máxima sin precondición temporal se vuelve «hazlo ya»
date: 2026-08-20
source: tecnocloud
tags: [prompts, agentes, voz, llm]
---

Puse al principio del prompt, con máximo énfasis: «ninguna llamada puede acabar sin registrar».
El agente empezó a registrar en el turno 2 y colgar: llamadas de 18-53 s (antes 115 s) sin preguntar
qué pasaba ni el nombre. Cumplía la regla al pie de la letra y destruía el servicio.

Tres errores que se refuerzan, y ninguno se ve leyendo el prompt:
1. **Obligación sin «cuándo»**: «X SIEMPRE» sin decir qué debe estar hecho antes se optimiza haciendo
   X cuanto antes. Hay que escribir el cuándo en la misma frase: «X es el CIERRE, nunca el principio».
2. **Valor de escape junto a la obligación**: ofrecer «si falta el nombre pon "No facilitado"» al lado
   del «registra siempre» es regalar el atajo. El escape va lejos, y marcado como último recurso.
3. La misma regla estaba en la `description` de la tool, que **pesa más que el prompt** — arreglar
   solo el prompt no habría servido. Las precondiciones duras van en la `description`.

Fix que sí discrimina: precondiciones explícitas y verificables en la tool («no ejecutes sin (1)
motivo concreto y (2) haber pedido el nombre»), y una cota de calidad legible por el modelo: «una
llamada de menos de un minuto en la que no has preguntado nada está mal atendida, aunque la registres».
Al añadir precondiciones, revisa los flujos que legítimamente no las cumplen (aquí «quiero hablar con
Silvia» no tiene aplicación ni síntoma) o reintroduces el fallo que arreglaste antes.
