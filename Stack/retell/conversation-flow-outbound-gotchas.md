---
title: conversation flow — tool calls fiables, naturalidad anti-IA y patrón outbound
date: 2026-06-11
source: sesión claude code — outbound reactivación Simarro (4 llamadas test)
tags: [retell, conversation-flow, outbound, voice, llm-bugs]
---

# Conversation Flow — gotchas de tool calls, naturalidad y outbound

Validado en llamadas reales (Simarro, flow `conversation_flow_29839e6fd152`, gpt-4.1). Aplica a cualquier Conversation Flow de Retell.

## Tool calls fiables (3 bugs reales del LLM)

### 1. El LLM alucina argumentos de tool aunque el dato NO exista en el flow
Caso: `Reservar` se llamó con `phone: "629127816"` (móvil del dueño) en vez de `{{telefono_lead}}`. El número tenía **0 apariciones** en el JSON del flow — alucinación pura, probablemente de memoria de entrenamiento o contexto de marca. Consecuencia real: lead y contacto Kommo creados con el teléfono equivocado y el WA de confirmación llegó al dueño.

**Fix**: para datos críticos (teléfono, email, ID) la instrucción del nodo function debe ser literal y cerrada:
> `phone`: EXACTAMENTE `{{telefono_lead}}` carácter a carácter — PROHIBIDO usar cualquier otro número, inventarlo o "recordarlo". SOLO cambia si el cliente ha dictado otro teléfono explícitamente en ESTA llamada.

### 2. Stall de promesas: promete info y nunca transiciona a la tool
Caso: "cuéntame un poquito más" → Ana dijo DOS veces "dame un momento y te cuento" sin llamar nunca a `Buscar_viviendas` (0 tool calls, sin transición). En un conversation node, hablar no dispara nada; si no hay edge que case con la intención, el LLM rellena con promesas vacías.

**Fix doble**: (a) edge directo del nodo conversacional al function node con condición explícita ("pide detalles / cuéntame más"); (b) regla en `global_prompt`: *PROHIBIDO PROMETER SIN ACTUAR — nunca digas "dame un momento" o "ahora te cuento" sin transitar a la tool en ese mismo turno*.

### 3. IDs fijados a dynamic var rompen la selección del usuario
Si `n_mirar`/`n_reservar` fijan `idealista_id={{vivienda_idealista_id}}`, cualquier reserva de una vivienda alternativa (matching o búsqueda en cartera) cae en el calendario/registro de la original.

**Fix**: la instrucción de la tool dice "el de la vivienda ELEGIDA" enumerando las fuentes posibles (original `{{var}}` / alternativa `{{var_match}}` / resultado de la tool de búsqueda).

### Bonus: nodo conversation "silencioso" = limbo
Un conversation node con instrucción "avanza sin hablar" nunca transiciona (la transición ocurre TRAS un turno hablado) → el flow se queda en limbo y el modelo alucina resultados ("tu visita está reservada" sin tool call). Eliminar el nodo o hacerlo hablar siempre.

## Naturalidad anti-IA (lo que delata a un agente de voz)

Detectado por el cliente en transcripción real ("se identifica que no es natural, ha sido como IA"):

1. **Empatía enlatada cada turno** — delator nº 1 ("entiendo perfectamente", "claro, lo comprendo" en 3 de 4 turnos). Regla: máximo UNA muestra de empatía en TODA la llamada y nunca abriendo el turno.
2. **Estructura fija acuse+contenido+pregunta** — prohibir el patrón; variar arranques.
3. **"¿Te parece?" como muletilla de cierre** — prohibida.
4. **Repetir la dirección completa** — solo la 1ª vez; después "esa", "la de Pozuelo".
5. **Inventar interpretación ante audio inaudible** — ante audio confuso: "perdona, ¿cómo dices?". Prohibido adivinar.
6. **Apertura con doble pregunta** — una sola pregunta en el primer turno.

**Voz en español**: `eleven_turbo_v2_5` suena robótica → `eleven_multilingual_v2` + `voice_temperature 1.1`. Trade-off de latencia asumible en outbound.

## Patrón outbound de reactivación

NO re-ofrecer a puerta fría la vivienda/producto que ya le interesó (si la descartó, re-venderla quema el lead). Camino correcto:
1. Mencionar la original con naturalidad ("vi que te interesaste por la de X… ¿qué pasó, sigues dándole vueltas?").
2. Sigue interesado → agendar. Descartó → **preguntar el motivo** (precio/zona/tamaño = señal de búsqueda).
3. Pivotar a una alternativa **personalizada** (RPC de matching pasada como dynamic vars desde el lanzador) o a búsqueda en cartera en vivo (tool).
4. Degradación limpia: sin matching → vars vacías → el flow cae al camino de descubrimiento puro.

Relacionado: [[prompt-engineering-voice-agents]], [[voice-config-inbound-castellano]].
