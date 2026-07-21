---
title: en un loop HITL, resuelve los turnos críticos (confirm/cancel/borrado/anáfora) deterministas antes del LLM
date: 2026-07-21
source: claude-code-session
tags: [agentes, hitl, interpreter, determinismo, agh]
---
El LLM mis-clasifica los turnos cortos y críticos de un loop HITL cuando hay algo pendiente. Casos
AGH reales: «bórrala» sobre un borrado pendiente → el LLM lo leyó CANCEL (canceló el borrado); «sí, y
además apúntame X» → lo leyó clarify («no te he entendido») y perdió confirmación + instrucción.

Patrón: esos turnos se reconocen DETERMINISTAS (regex/matchers exactos sobre texto normalizado) ANTES
de llamar al interpreter, no se delegan al modelo. Ya existía para el sí/no desnudo (#411); se extendió
a: anáfora de borrado con pending («bórrala» = confirm si el pending ES un borrado), y turno compuesto
«afirmación + conector + resto» (confirmar el pending + rutear el resto como turno nuevo, orquestado
FUERA del switch delicado para no tocarlo).

Ojo: los matchers de tokens exactos (tipo `bareHitlReply`) solo casan la palabra sola («si», no
«sí, gracias» ni «bórrala») → cada variante/compuesto hay que añadirla explícita.
Relacionado: [[guard-en-prepare-de-un-item-declina-el-batch-entero]] · [[agh-iberica]].
