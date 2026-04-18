---
title: toolHttpRequest sin parámetros + GPT-4.1 ignora tool calling
date: 2026-04-16
source: claude-code-session
tags: [n8n, gpt-4.1, tool-calling, handoff, chatbot]
---

En n8n, los nodos `toolHttpRequest` (tipo `@n8n/n8n-nodes-langchain.toolHttpRequest`) conectados como `ai_tool` al AI Agent permiten que el LLM haga llamadas HTTP como tools. Cuando estas tools **no tienen parámetros de entrada** (`placeholderDefinitions.values: []`), GPT-4.1 las ignora silenciosamente: produce el texto correcto que el system prompt le pide (ej: mensaje de despedida para handoff) pero **no ejecuta las tool calls**.

## Síntoma

- El AI Agent responde "Te paso con alguien del equipo" (texto coherente con el bloque `<handoff_humano>` del prompt)
- Pero las tools `Handoff asignar Ventas` y `Handoff etiquetar humano` NO aparecen en el execution log
- La ejecución del AI Agent tarda <1s (señal de que solo generó texto, sin tool calls)

## Fix validado

Reemplazar tool-calling por lógica determinista en el workflow:

1. El AI Agent emite un marcador textual `[HANDOFF]` al final de su mensaje de despedida
2. Un IF node `Es HANDOFF?` detecta el marcador en `$json.output`
3. Un Code node `Ejecutar handoff CW` ejecuta las HTTP calls directamente (`POST /labels`, `POST /assignments`)
4. El marcador se limpia del texto antes de enviarlo al cliente

## Cuándo aplica

Para cualquier acción crítica del workflow que dependa de que el LLM llame a una tool sin parámetros. No confiar en tool-calling para side-effects obligatorios — usar marcadores textuales + lógica determinista.
