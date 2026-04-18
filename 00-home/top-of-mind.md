---
title: top of mind
date: 2026-04-17
tags: [home, prioridades]
---

# Top of Mind

## Prioridades esta semana

- **Clinica Zen — pendientes post-migración**:
  - Añadir nodo Create Event en Leads entrantes (las reservas no crean evento en Google Calendar)
  - Cambiar Google Calendar ID de gonzalo al de CZ
  - Crear tipo de tarea "Cita asignada" en Kommo CZ UI, actualizar task_type_id en Especialista Asignado
- Notificaciones de tickets del dashboard a Slack `#01-tickets-soporte` con Bot incidencias
- Repo GitHub privado para skill chatbot-chatwoot-replicator

## Bloqueos activos

- Clinica Zen: pendiente scope "Chats" de Kommo (contactar soporte) — bloquea patrón Laserys para amojo_token dinámico

## Completado reciente

- Migración completa 9 workflows Clinica Zen: reset desde JSONs originales gonzalo + reemplazo de 30+ IDs/credenciales vía script Python + upload API
- Chatbot CZ testado end-to-end: reserva completa (WhatsApp → AI Agent → Kommo lead → email → Google Sheets)
- Fix chatbot flooding: debounce Redis 1s→10s, contextWindowLength 13→30
- Identificados salesbot IDs CZ (63808, 63810, 63812, 63814, 64322) y task types (1=Follow-up, 2=Meeting)
- Auditoría prompt Retell Clinica Zen: identificados 5 problemas
- Setup completo Obsidian + Claude Code + Daily Briefing + Slack bot
