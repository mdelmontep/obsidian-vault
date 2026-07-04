---
title: paso de elección conversacional — resolver la respuesta primero, la pregunta es el fallback
date: 2026-07-04
source: claude-code-session
tags: [onboarding, conversational, stt, nlu, fsm]
---

Una máquina de estados de onboarding/formulario que guarda "cualquier texto no vacío" como la respuesta del paso captura preguntas, órdenes, emoji, párrafos y correcciones como si fueran el dato. Bugs reales (AGH #76): "voz diego? a qué te refieres?" fijaba voz=diego; "recuérdame llamar a Dragados" quedaba como nombre del asistente.

Fix por paso:
1. Resolver la respuesta PRIMERO (match del valor esperado).
2. Si no resuelve, clasificar el turno: pregunta → explicar; orden/tarea → guiar; basura (emoji/puntuación/párrafo/longitud) → validar y re-pedir.
3. Interceptar "ayuda/¿qué sabes hacer?" en todos los pasos.

Gotcha voz/STT: el STT mete "?" por entonación → detectar pregunta por "?" da falsos positivos ("la femenina, no?" se rechazaba). En voz, resolver-primero y detectar pregunta por PISTAS/arranque interrogativo, no por el signo.

Auditar con N personas contra un arnés empírico (ejecuta el componente real, no especular) y filtrar ~50% FP. Ver [[slot-resolver-deterministic-pre-llm-nlu-regex-espanol]] · [[voice-agent-confunde-persona-interna-con-nombre-cliente]].
