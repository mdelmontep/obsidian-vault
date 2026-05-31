---
title: retell cambios al LLM sin publish del agente no afectan llamadas reales
date: 2026-05-01
source: claude-code-session
tags: [retell, voz, gotcha]
---

`PATCH /update-retell-llm/{id}` actualiza `general_prompt` y `general_tools`. Pero si el agente tiene `is_published: false`, los cambios solo se aplican al **playground**, NO a llamadas reales del número asignado.

Síntoma: cambias el prompt, funciona en playground, llamas al número → comportamiento viejo.

**Publish correcto (instancias con versioning, 2026-05+):**
`POST /publish-agent-version/{agent_id}` con `{"version": N}`. El antiguo `PATCH /update-agent {is_published:true}` ya **no** publica ahí.

**El LLM publicado es inmutable** → para editarlo:
1. `POST /create-agent-version/{agent_id}` con `{"base_version": N}` → crea draft N+1 (LLM también v N+1).
2. `PATCH /update-retell-llm/{id}?version=N+1` con los cambios.
3. `POST /publish-agent-version/{agent_id}` `{"version": N+1}`.

Verificar `GET /get-agent/{id}` → `is_published:true` + `version`/`response_engine.version` correctos. Probar comportamiento con [[retell-simulation-test-tool-mocks-y-sin-mock-e2e-real]].
