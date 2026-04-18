---
title: cambiar CW Enviar mensaje para usar token del bot en vez de Manuel
date: 2026-04-16
source: claude-code-session
tags: [inbox, pendiente, agentesia, chatwoot, n8n, chatbot]
---

El nodo `CW Enviar mensaje` del workflow `ChatBOT mejorado` (89B9QN23hOHDq6oP) usa el `api_access_token` de Manuel (`ST6t3xSRksMLaayFoHam8woM`) para enviar mensajes. Esto hace que los mensajes del bot aparezcan firmados por "Manuel" en la UI de Chatwoot.

Debería usar el access_token del Agent Bot (`ZFb8NqpiafGNHUbvbPNwkN3n`) para que aparezcan como "ChatBOT Agentesia".

Cambio: reemplazar el token en el header `api_access_token` del nodo `CW Enviar mensaje`.

## Tecnocloud — mismo pendiente

El workflow `Chatbot - FINAL` (id `LirbVJ9oIvLGENUQ`) en `n8ntecno.tecnocloud.es` también usa el token de usuario (`cZ2n6dBpQNoVLypDxAiqdEtC`) en vez del token del Agent Bot (`edLf39HmXwAPDrVjEBgwT86D`). Aplicar el mismo cambio.
