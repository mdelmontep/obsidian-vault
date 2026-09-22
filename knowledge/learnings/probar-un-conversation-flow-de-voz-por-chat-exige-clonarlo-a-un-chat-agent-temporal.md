---
title: probar un conversation flow de voz por chat exige clonarlo a un chat agent temporal
date: 2026-09-22
source: ecobox
tags: [retell, testing, conversation-flow]
---
Para recorrer un flow de voz por API (turnos de texto, sin llamar) Retell no deja atajos:

- `POST /create-chat` con el `agent_id` de voz → `Cannot start a chat session with selected agent.`
- `POST /create-chat-agent` apuntando a una versión publicada del flow → `Cannot specify version > 0 for new agent`.

Patrón que funciona: `create-conversation-flow` con una COPIA del flow de la versión a probar
(nodes + global_prompt + tools) → `create-chat-agent` sobre esa copia (versión 0) → `create-chat` +
`create-chat-completion` por turno → borrar el chat agent y el flow temporal al acabar (204).
Útil además para forzar condiciones: en la copia se puede fijar una hora de prueba (p. ej. un enum
de un solo valor en la tool de horario), cosa que el LLM ignora si solo se le pide en la descripción.
Las tools siguen llamando a los webhooks reales: registros y emails de prueba hay que limpiarlos después.

Caso: EcoBox v26 (22-sep-2026), escenarios dentro y fuera de horario. Ver [[clientes/ecobox/index|ecobox]].
