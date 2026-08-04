---
title: Prompt-only no garantiza que el LLM dispare la tool de aviso — necesita pre-check determinista
date: 2026-08-04
source: claude-code-session
tags: [llm, tool-calling, n8n, elphis, reglas-duras, prompt-engineering]
---

Cuando una regla dura exige "SIEMPRE responde X **y además** dispara la acción Y" (ej. aviso al equipo, email), instruir esto solo por prompt no lo garantiza: en una misma respuesta el LLM tiende a elegir **o** texto **o** tool_call, no ambos. Probado con gpt-4o-mini (Elphis, `router-ia`): con la regla en el system prompt, el modelo daba el texto de cara al usuario correcto ~100% de las veces, pero en la mayoría de variantes de la misma frase **no** llamaba a `pause_bot` — o sea, el usuario veía la respuesta bien pero el email al equipo no salía. Confirmado con batch de pruebas reales contra la API (no hipótesis): 0/3 dispararon la tool en un batch, 1/2 en otro.

Patrón correcto — el mismo que ya usa este bot para crisis suicida ([[llm-safety-critical-un-tool-no-cascada-de-tools]]): **pre-check determinista por regex ANTES de llamar al LLM**, no delegarlo al modelo. Si detecta el patrón, fija `reply_text` + dispara el aviso (subworkflow de notificación) sin pasar por el LLM en absoluto. El LLM solo decide en el resto de casos, donde no hay una acción obligatoria de por medio.

Regla general: si una instrucción de prompt combina "responde fijo" + "ejecuta una acción con efecto externo" (email, webhook, CRM), y el fallo silencioso importa (se pierde un lead, no se avisa a nadie), no confíes en que el LLM la cumpla de una sola pieza. Muévela a código determinista antes del LLM. Si solo es cara al usuario (sin efecto externo, ej. bloquear info sensible), el prompt-only sí es fiable — probado 4/4 con jailbreak incluido en el caso de composición de sustancias del mismo cliente.

Caso real: Centro Elphis, 2026-08-04. Alba reportó que el bot respondió sobre composición de una sustancia (tussi/heroína). Al añadir la regla de "ya tuve visita / ya hablé con vosotros" (debe avisar al equipo por email) solo en el prompt, el testing en vivo mostró que el aviso no se disparaba de forma fiable. Fix: nodo `Contacto previo pre-check` (regex) + `If contacto previo` + rama dedicada a `registrar-lead`, en paralelo a `Crisis pre-check`, en el workflow `router-ia` (n8n Elphis, ID `7huQC9GWl12SpYaE`).
