---
title: lock por conversación se libera tras responder, no tras el trabajo post-respuesta
date: 2026-07-21
source: claude-code-session
tags: [n8n, chatbot, concurrencia, chatwoot]
---
Orquestador de chat con lock distribuido por conversación (`slot_lock` por `conv:<id>`):
si el lock se mantiene hasta el FINAL del flujo y después de responder hay trabajo
lento (p.ej. extracción CRM con LLM ~12s), el lock queda retenido ~15s. Un 2º mensaje
del usuario que llega en esa ventana choca con el lock y, si el diseño lo DESCARTA
(202 locked_busy sin reintento), se pierde → el bot enmudece y el dato de ese mensaje
(p.ej. el nombre) nunca se procesa ni llega al CRM.

Fix doble: (1) liberar el lock + responder al webhook JUSTO tras enviar la respuesta
(el `respondToWebhook` no corta el flujo: la extracción sigue después, ya fuera del
lock); (2) en `locked_busy`, reintentar con espera corta (Wait 2.5s, máx N vía
`$runIndex`) en vez de descartar. Persistir en estado los ids creados en la parte
post-lock (2º upsert) para no perderlos / evitar duplicados en el siguiente turno.

Caso real: Elphis `chatwoot-event` — silencio tras dar el nombre + nombre vacío en
Clientify + "Timed out reading data" en Chatwoot, todo del mismo lock. Ver
[[n8n-status-success-no-implica-camino-critico]].
