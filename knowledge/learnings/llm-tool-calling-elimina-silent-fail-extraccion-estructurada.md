---
title: tool calling forzado elimina silent fail en extracción estructurada del LLM
date: 2026-05-18
source: claude-code-session
tags: [openai, llm, tool-calling, structured-outputs]
---

Patrón anti-pattern: pedir al LLM que termine cada respuesta con un bloque
JSON oculto (`<system_data>{...}</system_data>`) y parsear con regex. Con
system prompt largo (~6k tokens) + multi-idioma + temperatura > 0, el modelo
olvida el bloque ~5% de turnos. Parser regex devuelve `extracted_fields: []`
**silenciosamente** → progreso UI nunca avanza.

Fix correcto: function calling con `tool_choice` forzado.

```ts
client.chat.completions.parse({
  model: 'gpt-4o-2024-11-20',  // snapshot con Structured Outputs strict
  tools: [zodFunction({ name: 'emit_turn', parameters: schema })],
  tool_choice: { type: 'function', function: { name: 'emit_turn' } },
});
```

Beneficios:
- Modelo NO puede saltarse la tool (`tool_choice` forzado).
- Schema strict garantiza shape exacto.
- SDK auto-parsea con Zod (`parsed_arguments`).
- Falla → throw explícito en lugar de silent `[]`.

Fail-loud en parser, degradación graciosa en handler (mensaje
"disculpa, no he entendido" + audit log). La conversación no se rompe.

Ver también: [[llm-source-quote-anti-alucinacion-extraccion]]
