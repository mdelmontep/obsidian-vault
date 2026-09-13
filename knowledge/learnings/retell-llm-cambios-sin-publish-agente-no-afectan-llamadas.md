---
title: retell cambios al LLM sin publish del agente no afectan llamadas reales
date: 2026-05-01
source: centro-elphis
tags: [retell, voz, gotcha, despliegue]
---

`PATCH /update-retell-llm/{id}` actualiza `general_prompt` y `general_tools`. Pero si el agente tiene `is_published: false`, los cambios solo se aplican al **playground**, NO a llamadas reales del número asignado.

Síntoma: cambias el prompt, funciona en playground, llamas al número → comportamiento viejo.

**Publish correcto (instancias con versioning, 2026-05+):**
`POST /publish-agent-version/{agent_id}` con `{"version": N}`. El antiguo `PATCH /update-agent {is_published:true}` ya **no** publica ahí.

Dos formas de estrellarse con este endpoint, las dos medidas el 13-sep-2026 desplegando la v48 de Centro Elphis:

- **La versión va en el CUERPO, nunca como query param.** `?version=N` devuelve `400 {"error_message":"Unknown query parameter 'version'"}`. Como el endpoint existe, el 400 no delata que la forma sea otra — parece un rechazo de negocio.
- **Responde 200 con el cuerpo VACÍO.** Un cliente que haga `json.load(urlopen(...))` revienta con `JSONDecodeError: Expecting value: line 1 column 1 (char 0)` **después de haber publicado**. El traceback se lee como fallo y es éxito: si reintentas a ciegas, publicas dos veces. Tolerar el cuerpo vacío (`cuerpo = resp.read(); json.loads(cuerpo) if cuerpo.strip() else {}`).

Y publicar no se verifica por ausencia de excepción: comprobar que `max(v.version for v in get-agent-versions if v.is_published) == N`.

**El LLM publicado es inmutable** → para editarlo:
1. `POST /create-agent-version/{agent_id}` con `{"base_version": N}` → crea draft N+1 (LLM también v N+1).
2. `PATCH /update-retell-llm/{id}?version=N+1` con los cambios.
3. `POST /publish-agent-version/{agent_id}` `{"version": N+1}`.

Verificar `GET /get-agent/{id}` → `is_published:true` + `version`/`response_engine.version` correctos. Probar comportamiento con [[retell-simulation-test-tool-mocks-y-sin-mock-e2e-real]].
