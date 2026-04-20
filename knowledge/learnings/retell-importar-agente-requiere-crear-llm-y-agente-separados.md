---
title: retell importar agente requiere crear llm y agente separados
date: 2026-04-20
source: claude-code-session
tags: [retell, api, voice-agent]
---

## Problema

Importar un JSON de agente Retell desde el dashboard o la API falla con error 400 si:
- Tiene `retellLlmData` inline (el dashboard lo exporta así pero no lo acepta de vuelta)
- Tiene campos read-only: `agent_id`, `version`, `is_published`, `last_modification_timestamp`, `llm_id`
- `voice_id` no es un ID válido de `GET /list-voices`

## Solución

Crear en dos pasos:

1. `POST /create-retell-llm` con los datos del LLM (prompt, tools, begin_message, model)
2. `POST /create-agent` con `response_engine.llm_id` apuntando al LLM creado

## Voces en español

Consultar `GET /list-voices` y filtrar `accent: "Spanish"`. Formato: `{provider}-{name}`.
Voces femeninas españolas verificadas: `cartesia-Isabel`, `cartesia-Elena`, `qwen3-Sonrisa`.

## transfer_call

No funciona via API/JSON. Configurar desde el dashboard de Retell manualmente.

## Checklist pre-importación

1. Eliminar campos read-only del JSON
2. Verificar `voice_id` contra `/list-voices`
3. Crear LLM primero, agente después
4. `transfer_call` añadir desde dashboard
5. URLs de webhooks apuntan al dominio correcto (no EasyPanel)
