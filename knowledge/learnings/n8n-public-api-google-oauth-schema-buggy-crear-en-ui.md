---
title: n8n public api no permite crear google oauth via rest crear en ui
date: 2026-05-22
source: claude-code-session
tags: [n8n, oauth, google, api]
---

`POST /api/v1/credentials` con `type: googleCalendarOAuth2Api|googleDriveOAuth2Api|googleSheetsOAuth2Api` falla siempre por bug del schema:

```json
{
  "additionalProperties": false,
  "allOf": [{
    "if": {"properties": {"useDynamicClientRegistration": {"enum":[true]}}},
    "then": {"required": ["serverUrl"]},
    "else": {"not": {"required": ["serverUrl"]}}
  }, ...]
}
```

`useDynamicClientRegistration` NO está en `properties` y `additionalProperties: false` lo rechaza. Si lo omites, se evalúa como undefined → cae en el else → requiere NOT serverUrl pero al mismo tiempo el segundo allOf requiere clientId+clientSecret. Imposible satisfacer.

**Workaround**: crear las creds OAuth en n8n UI (browser). Requiere el OAuth dance manual de todas formas. Para automatizar, crear cred placeholder de tipo `httpHeaderAuth` y referenciarla — usuario completa en UI tras OAuth.

Casos donde sí funciona via API: `openAiApi`, `postgres`, `redis`, `smtp`, `httpHeaderAuth`, `telegramApi`.

Caso real: EcoBox 2026-05 — perdí 15 min hasta abandonar la idea y dejar workflows con cred-id placeholder.
