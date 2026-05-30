---
title: n8n AI Agent con Postgres Chat Memory no re-llama tool tras bugfix
date: 2026-05-30
source: claude-code-session
tags: [n8n, langchain, chat-memory, debugging]
---

Tras arreglar el código de una tool que estaba fallando, el LLM puede
seguir devolviendo el mismo mensaje de error **sin volver a invocar la
tool**. Causa: `memoryPostgresChat` (langchain) guarda los N turnos
previos (default 10), incluidos los `tool_calls` con su resultado de
error. El LLM lee ese historial y "aprende" que la tool falla → genera
la respuesta directamente desde contexto.

Síntoma:
- Tool arreglada y desplegada, pero ejecuciones nuevas tienen
  `tool_calls: 0` en el output del LLM.
- El user envía el mismo mensaje y recibe la misma respuesta de error.

Fix quirúrgico: purgar `n8n_chat_histories WHERE session_id = '<hash>'`.
El hash viene del nodo `Hash Session` o equivalente del workflow.
Crear workflow temporal con Webhook Trigger → Postgres node (DELETE
RETURNING) → llamar webhook → eliminar workflow.

Fix estructural (no aplicado): en el system prompt, instrucción tipo
*"si en el último turno la tool devolvió error pero el user lo
reintenta, DEBES volver a invocar la tool"*. Mitiga pero no garantiza
(LLM puede ignorarlo).

Aplica a cualquier AI Agent con memoria conversacional persistente —
no es n8n-specific.
