---
title: configurar crear-ticket en retell aia-llamadas
date: 2026-04-17
source: claude-code-session
tags: [inbox, pendiente, agentesia, retell, ticketing]
---

Los nodos del workflow AIA Llamadas (`O80k1QzfSkJUgzkD`) ya están creados:

- Switch Acción: 4o caso `Crear_ticket` (output 3)
- `Normalizar Datos Ticket` (Set) — extrae whatsapp_number, subject, description, priority, category, nombre de `body.args`
- `POST Crear Ticket` (HTTP Request) — POST al webhook del portal con `onError: continueRegularOutput`
- `Preparar Respuesta Ticket` (Code) — interpreta statusCode y devuelve `{status, mensaje}`
- `Respuesta Ticket` (respondToWebhook) — devuelve JSON a Retell
- `Respuesta Callback OK` (respondToWebhook) — **BUG FIX** para ruta `Solicitar_callback` que no tenía respond

## Pendiente (manual en dashboard Retell)

1. **Crear Custom Tool "Crear_ticket"** en el agente de voz Retell
   - URL: `https://n8n.agentesia.madrid/webhook/Reservas` (mismo webhook existente)
   - Parámetros: subject (string, req), description (string, req), priority (string, opt), category (string, opt), telefono (string, req), nombre (string, req)

2. **Actualizar prompt del agente de voz** — añadir sección "Soporte a clientes existentes" con flujo: confirmar cliente → escuchar → clasificar → usar Crear_ticket → interpretar respuesta

## Plan detallado

Ver plan completo en `/Users/manueldelmonte/.claude/plans/peaceful-gliding-feigenbaum.md`, secciones B.6 y B.7.
