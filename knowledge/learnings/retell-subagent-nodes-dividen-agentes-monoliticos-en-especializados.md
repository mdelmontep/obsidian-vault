---
title: retell subagent nodes dividen agentes monolíticos en especializados
date: 2026-04-18
source: retell-newsletter
tags: [retell, voice, arquitectura]
---
Retell lanzó Subagent Nodes (abril 2026) que permiten dividir un agente de voz monolítico en subagentes especializados con transiciones. Cada subagente tiene su propio prompt, tools y funciones. Patrón recomendado para clínicas: subagente "recepción" (saludo + identificación) → subagente "citas" (consulta disponibilidad + agenda) → subagente "transfer" (escalado a humano). Más fácil de debuggear que un prompt monolítico de 200 líneas.

Otras features relevantes del mismo release:
- JavaScript inline en conversation flow (cálculos, formateo fechas sin round-trip a n8n)
- SMS en llamada (confirmaciones de cita al paciente durante la llamada)
- Agent Timezone Settings (configurar Europe/Madrid por agente)
- Audio Testing desde nodo específico (debug sin pasar por flujo completo)
