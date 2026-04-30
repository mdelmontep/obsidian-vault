---
title: kommo webhook deja de disparar tras actualizar workflow en n8n
date: 2026-04-30
source: claude-code-session
tags: [kommo, n8n, webhook]
---

Tras hacer PUT a un workflow vía n8n API, Kommo puede dejar de enviar webhooks
a ese endpoint aunque el workflow esté activo y el URL responda correctamente.

- Ocurrido en CZ y Simarro al actualizar `QLfRT9AWmV1HLMZs` vía API
- n8n no notifica a Kommo del cambio → Kommo pierde el registro del listener

**Fix**: Ajustes → Integraciones → Webhooks en Kommo → borrar la URL afectada → volver a añadirla → Guardar.
Tarda segundos. Los mensajes vuelven a disparar inmediatamente.
