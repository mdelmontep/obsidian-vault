---
title: whatsapp await upsert antes de enviar botones interactivos
date: 2026-06-30
source: claude-code-session
tags: [whatsapp, meta, supabase, async, webhook]
---

El button_reply de Meta puede llegar antes de que un `upsert` fire-and-forget haya completado.

**Síntoma**: el handler del botón busca el intent en BD y no lo encuentra → "El documento ha expirado" aunque el usuario acaba de pulsar el botón.

**Causa**: en webhooks, el round-trip webhook→usuario→botón es casi instantáneo en móvil. Una escritura async no garantiza que esté en BD cuando vuelve el callback.

**Regla**: en cualquier flujo `escribe intent → envía mensaje interactivo → espera reply`, el insert/upsert debe ser `await` con guard de error antes del `send*`. Si falla la escritura, abortar y avisar al usuario antes de mandar el botón.

**Caso real**: `processMedia` en `/api/whatsapp/webhook` — upsert de `whatsapp_pending_intent` era `void`; fix `299d225a`.

Aplica a cualquier canal donde el callback llega por webhook separado (WhatsApp, Slack, Stripe webhooks con estado intermedio).
