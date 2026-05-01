---
title: retell cambios al LLM sin publish del agente no afectan llamadas reales
date: 2026-05-01
source: claude-code-session
tags: [retell, voz, gotcha]
---

`PATCH /update-retell-llm/{id}` actualiza `general_prompt` y `general_tools` del LLM. Pero si el agente que lo usa tiene `is_published: false`, los cambios solo se aplican al **playground** (test web), NO a llamadas reales del número asignado.

Síntoma: cambias el prompt, pruebas en playground (funciona), llamas al número (sigue con el comportamiento viejo).

Fix tras cambios sustanciales:
```bash
curl -X PATCH https://api.retellai.com/update-agent/{agent_id} \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d '{"is_published": true}'
```

Verificar con `GET /get-agent/{id}` → `is_published: true`. Cada nuevo PATCH al LLM o al agente puede requerir re-publicar (verificar comportamiento por versión de Retell).
