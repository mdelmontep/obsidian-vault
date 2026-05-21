---
title: llm tool-use con cards visuales — instruir explícito a no duplicar la lista
date: 2026-05-21
source: claude-code-session
tags: [llm, tool-use, system-prompt, ui]
---

Cuando una tool del LLM produce datos que la UI renderiza como card (tabla, lista, KPIs), el LLM duplica el contenido en su mensaje de texto si el system prompt no se lo prohíbe. Resultado: usuario ve la lista dos veces (card arriba + enumeración debajo).

Aplica a Anthropic tool-use y OpenAI function calling.

Fix en system prompt:

```
CUANDO HAY TOOL RESULT VISUAL:
- La interfaz renderiza una card con los datos. NO repitas la lista entera ni los importes uno a uno.
- Tu texto debe ser RESUMEN de 1-2 frases: titular, patrón observado, siguiente paso.
- Si truncated=true menciona que hay más y ofrece refinar.
```

Detectado en FacturaIA Copiloto PR-A3.1: `searchMovimientos` devolvía 8 movs, card mostraba todos, LLM además enumeraba "1. … 2. …". Tras la regla el LLM responde tipo "Tienes 8 pendientes: 4 cobros y 3 gastos. ¿Cuál quieres explorar?".

Relacionado: [[llm-tool-use-multi-turno-replay-tool-calls-y-results-emparejados]].
