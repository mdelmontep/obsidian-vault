---
title: workflow temporal webhook para operaciones bulk en google calendar
date: 2026-04-20
source: claude-code-session
tags: [n8n, google-calendar, patron]
---

Para crear N eventos en Google Calendar sin tener acceso directo al OAuth token (n8n no expone credenciales via API):

1. **Crear workflow temporal** via API:
   - Webhook trigger (POST `/crear_evento_test`)
   - Google Calendar Create (reutiliza credencial existente por ID)
   - Respond to Webhook (devuelve event_id)

2. **Activar** con `POST /api/v1/workflows/{id}/activate`

3. **Ejecutar N requests** con curl/python al webhook:
   ```json
   {"summary": "Valoración - Odontología - Ana López", "start": "2026-04-21T10:00:00+02:00", "end": "2026-04-21T11:00:00+02:00"}
   ```

4. **Desactivar y borrar** el workflow temporal:
   ```
   POST /api/v1/workflows/{id}/deactivate
   DELETE /api/v1/workflows/{id}
   ```

**Clave**: la credencial se referencia por ID (`"id": "oQIpq7KV7d6QW8rh"`) sin necesitar el token real.

Útil para: poblar calendarios de test, migraciones, limpieza masiva.
