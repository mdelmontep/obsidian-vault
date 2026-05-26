---
title: Retell `tool_call_strict_mode` solo valida args, no fuerza ejecutar el tool
date: 2026-05-25
source: claude-code-session
tags: [retell, tools, subagent]
---

`tool_call_strict_mode: true` en Conversation Flow valida que los argumentos cumplan el JSON schema del tool, pero NO obliga al LLM a invocar el tool. El LLM puede transicionar al siguiente nodo sin haberlo llamado nunca.

Síntoma típico: en subagent que tiene `Mirar_disponibilidad` declarado, el LLM dice "perfecto, te apunto a las 10:30" sin haber consultado la agenda — inventa la hora.

Fix combinado:
1. **Prompt explícito**: "OBLIGATORIO llamar X antes de proponer Y. Si no llamas X estás mintiendo al cliente."
2. **Transition condition exigente**: en el edge `transition_condition` poner `"Has llamado a X Y el cliente confirmó una HORA CONCRETA"` — el LLM debe poder demostrar que llamó al tool antes de transicionar.
3. **Tool description con precondición**: `description` del tool habla de pre-requisitos (ver [[llm-tool-description-precondiciones-pesa-mas-que-prompt]]).

Caso real: EcoBox `n-collect-date` 2026-05-25/26 — primer intento con strict_mode + prompt "obligatorio" insuficiente; añadir transition_condition explícita lo fijó.
