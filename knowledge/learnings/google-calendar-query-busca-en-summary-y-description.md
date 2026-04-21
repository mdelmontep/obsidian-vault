---
title: google calendar query busca en summary y description
date: 2026-04-21
source: claude-code-session
tags: [google-calendar, n8n, busqueda]
---

El parámetro `query` del nodo Google Calendar `getAll` en n8n hace búsqueda de texto libre en **summary + description** del evento.

Esto permite buscar eventos por un identificador (Lead_id, ticket_id, etc.) sin necesidad de guardar el `calendar_event_id` en base de datos. Basta con incluir el ID en la description al crear el evento.

**Patrón para cancelar/mover citas:**
1. Al crear evento: poner `Lead ID: 12345` en la description
2. Al cancelar: `getAll` con `query: "12345"` → devuelve el evento → `delete` con el `id` del resultado

**Limitación:** si el mismo ID aparece en varios eventos (ej: cita cancelada y re-creada sin borrar), la búsqueda devuelve todos. El workflow de cancelación borra todos los matches.
