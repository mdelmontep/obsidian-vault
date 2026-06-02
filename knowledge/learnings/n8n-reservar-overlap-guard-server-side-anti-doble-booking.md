---
title: anti-doble-booking necesita check de solapamiento server-side, no basta el event_id determinista
date: 2026-06-02
source: claude-code-session
tags: [n8n, google-calendar, booking]
---

El `event_id` determinista (hash phone+slot) SOLO evita que el MISMO teléfono reserve dos veces el mismo hueco. NO evita que **otro cliente** reserve la misma hora → doble-booking real (caso EcoBox: voz reservó sobre un evento ya existente a las 17:00).

Confiar en que el LLM llame `mirar_disponibilidad` antes es frágil. Fix server-side en `reservar_cita`: antes de crear, GCal getAll en la ventana `[preferred_date, preferred_date+duración]` (con `alwaysOutputData:true`), Code que filtra solapamientos reales (`start < before && end > after`), IF → si hay alguno responder `status:error` "hora ocupada" SIN crear ni notificar. Verificado: hueco ocupado rechaza, libre crea.

Ver [[n8n-webhook-tool-respond-no-hardcodear-exito-gatear-en-error-nodo]] · [[calendar-event-id-deterministico-sha1-phone-slot-anti-doble-booking]].
