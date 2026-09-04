---
title: tool description generica no fuerza ejecucion de tool critica
date: 2026-04-19
source: claude-code-session
tags: [n8n, ai-agent, tool-calling, bug, retell, elphis]
---

El nodo `Reservar_cita` (toolWorkflow) tenía una descripción de 74 caracteres: "Usa esta herramienta para reservar cita, una vez confirmada por el usuario". El LLM (GPT-5.1) generó texto de confirmación ("Te reservo a las 11:00") **sin ejecutar la tool**. La cita nunca se registró.

## Fix

Expandir la descripción a ~280 chars explicando las **consecuencias de no llamar**:

> "OBLIGATORIO para registrar una cita. Usa esta herramienta SIEMPRE que el paciente confirme la reserva. Sin ejecutar esta herramienta, la cita NO queda registrada en el sistema aunque hayas escrito un mensaje de confirmación. Necesita: nombre, teléfono, email, servicio, fecha y hora."

Además, reforzar en el system prompt:
- Regla crítica #1: "SIEMPRE ejecuta Reservar_cita cuando el paciente confirme"
- En el paso de reserva: "OBLIGATORIO. SIN ESTA LLAMADA LA CITA NO EXISTE"
- En el paso post-reserva: "Solo DESPUÉS de que Reservar_cita se ejecute con éxito"

## Patrón general

Para toda tool que realice una **acción de escritura irreversible** (reservar, cancelar, enviar email, crear registro), la descripción debe:
1. Decir que es OBLIGATORIA en el contexto correspondiente
2. Explicar qué pasa si NO se llama (la acción no ocurre)
3. Listar los parámetros requeridos

Una descripción genérica de una línea no es suficiente — el LLM la trata como opcional.

## Complemento (2026-05-03)

Si la description ya es agresiva pero el agente sigue fabulando (ej. inventa slots de calendario sin llamar `Mirar_disponibilidad`): bajar `temperature` a `0`. Síntoma diagnóstico: ejecución con `intermediateSteps=0` cuando debería haber al menos 1 tool call.

## Complemento (2026-08-04) — ni reforzando el prompt se garantiza

Caso Elphis: regla dura en el prompt ("di EXACTAMENTE X y llama YA a pause_bot") con instrucción muy directiva. Probado en vivo contra la API real (gpt-4o-mini): el modelo decía el texto correcto la mayoría de las veces, pero en la mayoría de esas veces **no llamaba a la tool** — content y tool_call parecen mutuamente excluyentes en una misma respuesta cuando el modelo "decide hablar". 0/3 y 1/2 en dos tandas de prueba con frases casi idénticas.

Cuando la tool dispara un efecto externo obligatorio (email, webhook, CRM) y el fallo silencioso importa, no hay cantidad de prompt engineering que lo garantice — hace falta mover la detección a código determinista **antes** del LLM (mismo patrón que ya usa este proyecto para crisis: regex pre-check → si hay match, ni se llama al LLM, se fuerza la acción). Si la regla es solo cara al usuario sin acción externa (ej. bloquear una respuesta), el prompt-only SÍ es fiable — 4/4 en el mismo caso real, jailbreak incluido.

En Retell Conversation Flow (a diferencia de n8n) no existe esa capa de código — las transiciones son siempre `type: prompt` evaluadas por el modelo. Ahí el máximo disponible es ampliar las condiciones de transición + ejemplos few-shot, sin garantía dura.

## Complemento (2026-08-12) — misma reincidencia, dos sistemas distintos el mismo día

Simarro, voz (Retell Conversation Flow): el nodo `n_proponer_hora` dijo "un agente te contactará" — frase reservada por regla dura del `global_prompt` a DESPUÉS de ejecutar `Reservar` — sin haberla ejecutado. Reforzada la prohibición LOCALMENTE en el nodo (no solo en el prompt global).

Mismo día, Simarro WhatsApp (LangChain AI Agent, no Retell): regla explícita "ANTES de decir 'no operamos', llama `Buscar_viviendas`" — el LLM respondió la negación directamente, sin invocar la tool. Confirmado con los logs de ejecución de n8n: cero llamadas a la tool en ese turno. Reforzado con "PROHIBIDO ABSOLUTO... ni aunque estés seguro" — mismo tipo de parche que arriba, mismo tipo de garantía (ninguna dura).

Confirma el patrón de la entrada de abril con dos arquitecturas de agente distintas (conversation-flow por nodos vs. LangChain AI Agent con tools) el mismo día: una regla condicional "antes de X, verifica con la tool" en prompt/systemMessage se salta más fácilmente cuantas más veces el LLM "cree" conocer la respuesta sin buscar. Reforzar el texto mitiga pero no garantiza — ver el complemento de agosto arriba sobre mover la detección a código determinista cuando el fallo importa de verdad.

## Complemento (2026-09-04) — la variante peor: el prompt nombra una tool que NO EXISTE

Chatbot propio de Agentesia (`89B9QN23hOHDq6oP`, WhatsApp). El system prompt mandaba `Llama a "Agendar"`; el nodo real se llama `Reservar`. El agente cerró la demo, dijo la fecha y la hora, avisó a Slack y registró el lead — **sin crear el evento**. Ejecución en `success`.

Lo contraintuitivo, y me equivoqué razonándolo al revés: **el system prompt no determina qué tools ve el LLM**. El modelo ve `name` + `toolDescription` de cada nodo. Por eso convivían, en la MISMA conversación:

- `Lead caliente` y `Lead cita DEMO` → `descriptionType: manual`, descripción escrita a mano → **ejecutadas**, aunque el prompt las llamaba `Notificar Callback` y `Notificar Demo` (nombres inexistentes).
- `Reservar`, `Mirar Dispo`, `Registro Sheets` → `descriptionType: auto` (n8n autogenera una genérica) → solo se ejecutó `Mirar Dispo`, la única que el prompt nombraba bien.

Regla: al auditar un AI Agent, cruzar `[n.name for n in nodes if 'Tool' in n.type]` contra los nombres citados en el `systemMessage`. Y poner `descriptionType: manual` en **toda** tool de escritura, no solo en las que fallan.

Diagnóstico que zanja la discusión, sin releer prompts: `GET /api/v1/executions/{id}?includeData=true` → `.data.resultData.runData | keys` lista las que corrieron **de verdad** en esa ejecución. Ver [[ejecucion-en-verde-no-prueba-el-efecto]] · [[error-de-tool-de-ai-agent-no-marca-la-ejecucion-como-fallida]]
