---
title: amojo api v1 requiere token centrifugo, no oauth2
date: 2026-04-17
source: claude-code-session
tags: [kommo, amojo, n8n]
---

La API de chat de Kommo (`amojo.kommo.com/v1/chats/{amojo_id}/{chat_id}/messages`) usa un token de sesión Centrifugo propio en el header `X-Auth-Token`. Este token:

- **Expira cada ~24 horas**
- **NO es el OAuth2 access_token** ni el Long Lived Token — ambos dan 401 en ese endpoint
- Se obtiene originalmente desde el navegador (DevTools → Network → buscar requests a `amojo.kommo.com`)

La única forma automatizada de obtenerlo es el **patrón Laserys**:

```
POST {account_url}/ajax/v1/chats/session
Headers:
  Authorization: Bearer {oauth2_access_token}
  X-Requested-With: XMLHttpRequest
Body:
  request[chats][session][action]=create
```

Respuesta relevante:
- `response.chats.session.access_token` → amojo_token fresco
- `response.chats.session.account.id` → amojo_id

**Requisito crítico**: el OAuth2 debe tener scope **"Chats"**. Sin ese scope, el endpoint devuelve 403.

En el workflow, cada bloque de envío llama primero a este endpoint para obtener un token fresco → eliminando la expiración como problema.
