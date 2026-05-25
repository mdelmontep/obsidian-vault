---
title: tool description con precondiciones pesa más que el system prompt para evitar tool-call temprano
date: 2026-05-25
source: claude-code-session
tags: [llm, tool-calling, retell, openai, prompt-engineering]
---

Si el LLM dispara una tool antes de tener los datos que el flujo necesita, **no basta con escribirlo en el system prompt** ("PROHIBIDO ejecutar X antes del paso Y"). El LLM lo ignora cuando ve oportunidad de invocar la tool.

Lo que sí funciona, en orden:

1. Poner las precondiciones explícitas en el `description` de la propia tool ("Llamar SOLO al cierre. Requisitos: nombre del cliente recogido, motivo entendido, fase de cierre. PROHIBIDO en turnos 1-2").
2. Activar `tool_call_strict_mode: true` (Retell) o equivalente para que params vacíos no se acepten.
3. Aclarar en cada `parameter.description` qué no es válido (ej. `nombre_cliente` ≠ persona solicitada).

Caso real Tecnocloud (2026-05-25): Laura disparaba `registrar_llamada` en turno 1 incluso con bloque "PROHIBIDO antes del paso 3" + "NO ejecutes ninguna tool en este turno" en el prompt. Se contuvo solo tras mover esas reglas al `description` de la tool.

Universal a cualquier LLM con function calling (OpenAI, Anthropic, Retell, etc.).
