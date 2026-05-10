---
title: n8n gmail node nativo no soporta headers custom
date: 2026-05-09
source: claude-code-session
tags: [n8n, gmail, email]
---

El nodo `Gmail` nativo de n8n (OAuth2) NO expone parámetros para headers
arbitrarios `X-*`. Solo permite To/Cc/Bcc/Subject/Body/Attachments.

Si necesitas inyectar header custom (p.ej. para que un poller del propio
panel ignore self-emails), opciones:

1. **HTTP Request → `gmail.users.messages.send`** con `raw` base64
   (RFC822 MIME que tú construyes y donde añades los headers).
2. **Estrategia alternativa más simple**: filtrar por `From: ===
   oauth_email` en el ingestor — ver
   [[gmail-poll-debe-filtrar-self-sender]]. Suficiente cuando el sender
   del bot es predecible.

Caso real Tecnocloud: necesitaba `X-Tecnocloud-Source: voice-bot` para
distinguir emails del bot n8n; el nodo Gmail no lo permitía → resolví
filtrando por From. Sin re-ingeniería del nodo.
