---
title: crear-ticket en retell aia-llamadas — completado
date: 2026-04-18
source: claude-code-session
tags: [completado, agentesia, retell, ticketing]
---

Integración de ticketing en el agente de voz Retell completada (2026-04-18).

## Implementado

- **Retell LLM** (`llm_190533919a5b834eb3ceabebf0fe`): tool `Crear_ticket` + sección SOPORTE en prompt
- **Prompt SOPORTE**: flujo IDENTIFICAR (empresa, nombre, teléfono) → ENTENDER (servicio, problema, desde cuándo) → CLASIFICAR → Crear_ticket → confirmar
- **404**: redirige a WhatsApp 919 933 525 (no transfer_call)
- **Anti-callback**: incidencias siempre van a ticket, nunca a Solicitar_callback
- **Cierre cálido**: variado, sin repetir info

## Workflow n8n (`O80k1QzfSkJUgzkD`)

- Switch Acción output 3 → Normalizar Datos Ticket → POST Crear Ticket → Preparar Respuesta Ticket → Respuesta Ticket
- `Normalizar Datos Ticket` lee de `$('Webhook').first().json.body.args.*` (no de `$json.body`)
- `POST Crear Ticket` usa URL interna Docker: `http://agentesia-dashboard-interno-tpiuu8:3000`
- `Preparar Respuesta Ticket` parsea statusCode de `error.message` (AxiosError)
- Mensajes Slack con tag `- Retell (llamada de voz)` para identificar origen

## Pendiente

- Test con llamada real a un cliente registrado en el portal
- Borrar tickets de test del portal (cuando haya acceso)
