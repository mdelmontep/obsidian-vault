---
title: notificaciones tickets dashboard a slack
date: 2026-04-18
source: claude-code-session
tags: [inbox, pendiente, agentesia, slack, ticketing]
---

Tarea pendiente (ya en canvas Slack #01-tareas-pendientes):

Cuando se cree un ticket desde el dashboard de clientes (`clientes.agentesia.madrid`), enviar mensaje automatico a `#01-tickets-soporte` (C0ATLH1H8E4) usando el bot "Bot incidencias".

Incluir en el mensaje: ID ticket, cliente, asunto, prioridad.

Implementar en el backend del portal (webhook post-create o evento en el endpoint `/api/webhooks/whatsapp-ticket`).
