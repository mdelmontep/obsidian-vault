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

**Un matcher que corta el turno antes del LLM ROBA turnos, así que su vocabulario compite con tres cosas, no una** (30-jul, #672):
1. Los otros matchers — los guards deben ser disjuntos **por construcción** (`pending > 0` vs `=== 0`), no por su orden en el fichero.
2. **Las copias de error del propio sistema.** El generic decía «Inténtalo de nuevo en un momento» y el matcher se quedaba `inténtalo de nuevo`: un read revienta → el agente lo sugiere → el usuario lo repite → se le proponen cinco altas que nadie pidió en ese turno. El sistema pone palabras en la boca del usuario: hay que grepear las **plantillas de respuesta**, no solo el código de ruteo.
3. El habla real con ASR: ampliar los BORDES (prefijos «venga/pues», sufijos «por favor/ya») es seguro; relajar el ancla `^…$` no, porque es lo único que separa una referencia de un re-dictado con contenido nuevo.

Corolario: una forma genérica que no identifica el OBJETO sobre el que actuar («inténtalo otra vez» no dice qué reintentar) no puede casar mientras no exista un puntero específico para ese objeto.

Relacionado: [[guard-en-prepare-de-un-item-declina-el-batch-entero]] · [[un-puntero-durable-a-una-fila-borrada-convierte-un-fallo-en-bucle]] · [[agh-iberica]].
