---
title: una regla de prompt que el modelo cumple a medias suele ser decidible en código — compruébalo DESPUÉS, no reescribas el prompt
date: 2026-08-04
source: claude-code-session
tags: [agentes, llm, prompt, determinismo, agh]
---
Caso AGH (#237, medido n=25 entrelazado): «con 2+ oportunidades recientes, "súbela a 80k" NO debe
elegir título a ciegas». La regla lleva meses en el `SYSTEM_PROMPT` y **`main` la cumple 15/25 (60 %)**
— nadie lo sabía porque el eje agregado la tapaba.

La pregunta que ahorra la ruleta de redacciones: **¿es decidible sin el modelo?** Aquí sí — *si el
título emitido no aparece en lo que dijo el usuario, el modelo lo ha inferido*. Comprobación en
código, post-hoc: **1-2/25 → 25/25**, y arregla también el flake previo que se daba por varianza
aceptada.

Dos condiciones para que sea barato:
- **Va DESPUÉS del LLM, no antes.** No roba turnos ni compite con otros matchers —el riesgo de
  [[hitl-turnos-criticos-deterministas-antes-del-llm]]—: solo quita un campo que el modelo no podía
  saber, y el camino de ambigüedad que ya existía hace el resto.
- **No parsea copia de presentación.** Bastaba CONTAR cuántas candidatas hay en contexto; parsear su
  `label` («título» de Cliente) habría sido una tercera copia del formato capaz de divergir.

Corolario: perseguir con redacciones una regla que el modelo obedece a medias es caro y acoplado
([[un-prompt-es-una-superficie-con-localidad-no-un-documento]]). Primero mira si la puedes decidir.
