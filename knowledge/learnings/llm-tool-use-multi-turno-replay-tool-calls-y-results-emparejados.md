---
title: llm tool-use multi-turno requiere replay de tool_calls y tool_results emparejados
date: 2026-05-20
source: claude-code-session
tags: [llm, openai, anthropic, tool-use, persistence]
---

Persistir `tool_calls`+`tool_results` del LLM juntos en una sola fila `rol='assistant'` (JSON) es razonable, pero el replay debe re-emitir cada `tool_result` inmediatamente después del assistant que lo invocó, no en una "fila tool" separada que nunca existirá.

- **OpenAI**: 400 `"tool_call_ids did not have response messages"` si un assistant con `tool_calls` no es seguido por `role:'tool'` por cada `call_id`.
- **Anthropic**: 400 equivalente con `tool_use` sin `tool_result` block.

Síntoma: 1er turno OK, 2º turno rompe (es cuando entra el replay).

Hardening: descartar `tool_calls` huérfanos (sin `tool_result` emparejado por id) al replay — threads viejos pre-fix tendrán filas rotas y romperán otra vez si no se filtran.

Caso real: facturaia Copiloto v2 commit `380110c` (2026-05-20).
