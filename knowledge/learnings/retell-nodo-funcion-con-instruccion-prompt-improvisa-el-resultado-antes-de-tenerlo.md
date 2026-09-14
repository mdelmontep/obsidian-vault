---
title: retell nodo función con instrucción prompt improvisa el resultado antes de tenerlo
date: 2026-09-14
source: centro-elphis
tags: [retell, conversation-flow, voz, tools]
---

Un nodo `function` de un conversation flow con `speak_during_execution: true` e `instruction.type: "prompt"` deja al LLM hablar **mientras** la tool corre, y el LLM rellena con lo que cree que va a pasar: «Avisamos al equipo ahora mismo… hasta luego» antes de que exista el resultado. La despedida y la promesa salen aunque la tool falle, y el nodo siguiente (el cierre) repite o contradice.

Síntoma: frases de cierre o de confirmación pegadas justo antes del `tool_call_invocation` en el transcript; en llamada real, la persona cuelga antes de que el cierre diga lo que la tool devolvió.

Fix: `instruction: {"type":"static_text","text":"Un momento."}`. El texto fijo no puede anticipar nada; el cierre habla con el resultado ya en contexto.

Gotcha del medidor: el juez de simulaciones de Retell puede marcar ese «Un momento.» como «narra lo que hace». Verificar por transcript antes de dar el caso por fallido.

Caso real Elphis 14-sep (voz v50, `fn_crear_lead`): visto en la llamada de un paciente del 9-sep y en la primera tanda de simulación; tras el cambio, 9/9 recados correctos por transcript. → [[clientes/centro-elphis/index|centro-elphis]]
