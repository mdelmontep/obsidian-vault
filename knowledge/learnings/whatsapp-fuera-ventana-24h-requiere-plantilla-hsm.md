---
title: whatsapp fuera de la ventana de 24h exige plantilla HSM aprobada
date: 2026-06-24
source: claude-code-session
tags: [whatsapp, meta, arquitectura]
---
Texto libre (Cloud API o vía Chatwoot) solo se entrega <24h desde el último
mensaje del cliente. Cualquier mensaje proactivo / re-engagement (recordatorio,
aviso) fuera de esa ventana DEBE ser plantilla HSM aprobada por Meta, o Meta lo
rechaza.

Patrón cuando lo dispara una app: la app NO manda texto libre directo; dispara un
evento a n8n y n8n envía la plantilla. La app sella estado idempotente (p.ej.
`last_reminder_sent_at` con guard `is null`) y NO inyecta el texto en el hilo (lo
posee la plantilla, no se puede reconstruir fiel).

Bot voz+chat, mismo mensaje (p.ej. enlace de cita) por canal distinto: **chat**
(el paciente escribió → ventana abierta) = texto libre; **voz** (solo llamó, nunca
escribió → business-initiated) = plantilla HSM. Decidir por presencia de `conv_id`.
Y en chat, en vez de mandar por Cloud API directo (invisible en la bandeja), postear
el saliente como `message_type:outgoing` en Chatwoot: el propio webhook lo reenvía a
WA (path `send_to_meta`) → sale Y queda visible en el timeline.

Caso real: recordatorio de inactividad onboarding agency-portal (PR #95) → workflow
n8n "AIA Onboarding — Research y arranque", case `event=onboarding_reminder` → nodo
Meta Cloud API. Elphis 2026-07-21: `book-and-notify` enlace Doctoralia chat→Chatwoot
/ voz→plantilla `elphis_cita_link`. Ver [[n8n-api-put-workflows-rechaza-settings-desconocidos]].
