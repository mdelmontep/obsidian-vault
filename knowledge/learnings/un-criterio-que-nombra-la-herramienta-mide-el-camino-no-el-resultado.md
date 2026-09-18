---
title: un criterio que nombra la herramienta mide el camino, no el resultado
date: 2026-09-18
source: elphis (suite de simulación Retell, caso «ingreso residencial»)
tags: [testing, agentes-voz, retell, metodo, gates]
---

Un caso de la suite llevaba 11 corridas en rojo y estaba anotado en el vault como **bloqueante del
proyecto**. Su criterio: «el agente llama a la herramienta `crear_lead`». La simulada pedía cita, el
flujo salía por `reservar_visita`, y ese workflow crea **la misma ficha** en el CRM. El resultado de
negocio se cumplía; lo que fallaba era el criterio, que fijaba el camino.

- Criterio de camino: «llama a `crear_lead`» → se rompe cada vez que el flujo gana una ruta nueva.
- Criterio de resultado: «registra el contacto antes de colgar: `crear_lead` **o** `reservar_visita`».
- **El daño no es el falso rojo, es el sitio que ocupa**: la rama que sí falla no tenía caso. Al
  escribirla (ingreso + NO quiere cita) salió el defecto real: 2 de 5 llamadas acaban en `end_call`
  sin registrar nada. El rojo falso llevaba semanas tapando al verdadero.

Regla: ante un rojo, antes de tocar el sistema, lee la transcripción y pregunta si el criterio exige
el **resultado** o una **implementación** de él. Un criterio por herramienta caduca con el diseño.
Ver [[la-transcripcion-de-un-test-que-pasa-es-donde-esta-el-defecto-que-nadie-mide]] ·
[[un-gate-anclado-a-un-diseno-no-desplegado-falla-identico-contra-todo-y-deja-de-medir]]
