---
title: n8n contextWindowLength bajo hace que el agente repita preguntas ya contestadas
date: 2026-04-18
source: claude-code-session
tags: [n8n, ai-agent, memoria, chatbot]
---

`contextWindowLength` en `memoryPostgresChat` controla cuántos mensajes previos se inyectan en el contexto del LLM. Con valor 13 (por defecto en algunos workflows), el agente pierde contexto rápido y repite preguntas que el usuario ya contestó.

Valor recomendado: 30. Suficiente para una conversación de reserva completa (nombre, teléfono, servicio, fecha, hora, confirmación) sin perder ningún turno.

Síntoma: el bot pregunta "¿cuál es tu nombre?" después de que el usuario ya lo dio 3 turnos antes.
