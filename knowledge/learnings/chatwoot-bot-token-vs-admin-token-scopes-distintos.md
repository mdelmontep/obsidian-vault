---
title: chatwoot bot token no sirve para operaciones admin usar login admin
date: 2026-05-22
source: claude-code-session
tags: [chatwoot, api, auth]
---

Chatwoot tiene 3 tipos de tokens distintos con scopes muy diferentes:

1. **Agent API token** (Profile → Access Token, per-user) — operaciones normales como ese user.
2. **Bot token** (agent_bot.access_token) — SOLO postear/leer mensajes en conversaciones asignadas a ese bot. 401 en `/profile`, `/inboxes`, `/labels`, `/custom_attribute_definitions`.
3. **Platform API key** (superadmin) — gestión multi-account.

Para crear inbox/labels/custom-attrs/agent-bots via API: usar token de un agente Administrator obtenido por login:

```bash
curl -X POST https://chatwoot.../auth/sign_in \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@...","password":"..."}'
# devuelve {data: {access_token: "..."}}
```

Ese `access_token` se manda como header `api_access_token: <token>` en endpoints `/api/v1/accounts/{id}/*`.

Caso real: EcoBox 2026-05 — perdí 5 min con bot token (`/profile` daba 401) hasta cambiar a login admin.
