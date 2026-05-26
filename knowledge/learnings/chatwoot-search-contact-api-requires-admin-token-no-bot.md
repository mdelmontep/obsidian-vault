---
title: Chatwoot `/contacts/search` API requiere admin token, no bot token
date: 2026-05-25
source: claude-code-session
tags: [chatwoot, api, permissions]
---

Endpoint `GET /api/v1/accounts/{id}/contacts/search?q=...` devuelve `"Authorization failed - please check your credentials"` con bot user_access_token (auth `api_access_token`). El mensaje de descripción aclara: `"Access to this endpoint is not authorized for bots"`.

Causa: Chatwoot restringe búsquedas globales a roles admin/agent. Los bots no pueden listar/buscar contactos arbitrarios (medida razonable contra abuso).

Workarounds:
1. **Admin cred separada en n8n**: crear `httpHeaderAuth` con admin user_access_token (no bot). Riesgo: token con más alcance del necesario.
2. **Evitar el endpoint**: si tienes `contact_id` o `conversation_id` directos, usar `GET /contacts/{id}` o `GET /conversations/{id}` que sí aceptan bot token.
3. **Buscar en otra fuente**: en EcoBox movimos Buscar_reserva de Chatwoot a Google Calendar directo (donde Reservar ya guardaba `Tel:+34...` en description).

Caso real: EcoBox `Buscar_reserva` 2026-05-25 — devolvía `found:false` en todas las llamadas hasta reescribir contra GCal.
