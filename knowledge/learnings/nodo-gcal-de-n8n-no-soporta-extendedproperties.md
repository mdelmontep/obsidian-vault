---
title: nodo gcal de n8n no soporta extendedProperties — http request con credencial predefinida
date: 2026-08-24
source: elphis-psicologia
tags: [n8n, google-calendar, idempotencia]
---
El nodo Google Calendar de n8n no permite escribir `extendedProperties` en el create
ni filtrar con `privateExtendedProperty` en el getAll. Para el patrón de idempotencia
"bookingKey en el evento" hay que ir por **HTTP Request** con
`authentication: predefinedCredentialType` + `nodeCredentialType: googleCalendarOAuth2Api`
(misma credencial OAuth, sin duplicar nada):
- lookup: `GET /calendars/{id url-encoded}/events?privateExtendedProperty=bookingKey%3D<k>`
- create: `POST .../events` con `extendedProperties.private.bookingKey` en el body.
Patrón completo (idempotencia doble Redis + bookingKey, relectura tight del hueco):
`elphis-psicologia/infra/README-agenda.md`. Los nodos GCal normales (getAll/update/
delete) siguen valiendo para lo demás. Ver [[lock-e-idempotencia-en-n8n-con-redis-incr-sin-set-nx]]
