---
title: borrar 2 eventos duplicados de Laura Gomez en Google Calendar Leads Agentesia
date: 2026-04-15
source: claude-code-session
tags: [inbox, pendiente, agentesia, google-calendar, limpieza]
---

Durante los tests del workflow `Web Chat Agentesia` (ID `G8vbSYm0SY3zi912`), se crearon **dos eventos duplicados** de demo en el calendar `Leads Agentesia` que hay que borrar manualmente.

## Qué hay que borrar

Ambos eventos están en el calendar `Leads Agentesia` (ID `c_9d60e09dfaa1c27ff780d83f8fb7071576178ba95e0b3be3f22cc5112a9505e6@group.calendar.google.com`), fecha **jueves 2026-04-16 a las 11:00**:

1. Evento con datos incompletos — `Summary: Demo AgentesIA - (Taller mecánico)`, descripción con `Cliente:` y `Teléfono:` vacíos. Creado en ejecución 548 durante el test del bug de Reservar prematuro.
2. Evento con datos completos — `Summary: Demo AgentesIA - Laura Gomez (AutoFix Rozas)`, descripción completa. Creado en ejecución 549 inmediatamente después.

Ambos son **falsos positivos de test**, no hay ningún cliente real llamado Laura Gomez con una demo agendada.

## Por qué no los borré

Acción destructiva sobre recurso compartido (Google Calendar de producción). Requiere aprobación explícita y acceso interactivo al calendar.

## Cómo borrarlos

- Opción A: abrir el calendar `Leads Agentesia` en Google Calendar, ir al jueves 16/04 11:00 y borrar los dos eventos
- Opción B: via API de Google Calendar si se tiene el `eventId` — se puede recuperar listando eventos del rango y filtrando por `summary LIKE '%Laura Gomez%' OR summary LIKE '%(Taller mecánico)%'`
