---
title: retell simulation testing — tool_mocks para el LLM, sin-mock para E2E real
date: 2026-05-31
source: claude-code-session
tags: [retell, voz, testing, n8n]
---

Verificar un agente de voz sin gastar llamadas reales, vía API de Retell:
`POST /create-test-case-definition` (user_prompt = persona/goal, `metrics` en lenguaje natural, `tool_mocks` opcionales) → `POST /create-batch-test` → `GET /v2/list-test-runs/{batch_id}` (status + `result_explanation` + `transcript_snapshot`).

Dos modos según qué quieras probar:
- **Con `tool_mocks`**: la respuesta del tool se simula → pruebas SOLO el comportamiento del LLM (que pida el dato, que elija de la lista, que derive) sin tocar n8n/Kommo/calendar.
- **Sin mockear un tool**: el simulador llama al **webhook real** con `call_id "playground"` válido → **E2E auténtico** (crea lead, evento, etc.).

Clave: un `curl` directo al webhook de reserva NO completa el flujo si éste depende del contexto de llamada (`call_id` Retell) — el simulador sin-mock sí, porque genera un call_id válido. Si tu instancia n8n no retiene ejecuciones, verifica por efecto (consultar calendar/Kommo). Ver [[retell-llm-cambios-sin-publish-agente-no-afectan-llamadas]].
