---
title: kommo scope chats puede no aparecer en ui, contactar soporte
date: 2026-04-17
source: claude-code-session
tags: [kommo, oauth2]
---

El scope "Chats" (necesario para usar el Chat API / patrón Laserys de token dinámico) puede **no aparecer** como opción al crear o editar integraciones privadas en Kommo.

Intentos fallidos:
- Editar la integración existente → no aparece
- Crear una integración privada nueva → tampoco aparece
- Verificado en cuenta con el mismo plan que otra cuenta que sí lo tiene

Solución: contactar `support@kommo.com` pidiendo habilitar el Chat API scope. Según la documentación oficial de Kommo, el Chat API debería estar disponible para integraciones privadas ("The ability to create integration with different messengers").

La página de permisos de la documentación (`developers.kommo.com/docs/permissions`) no lista scopes individuales, así que no hay forma de verificar disponibilidad por documentación.

Alternativa descartada: la Chat Channels API v2 (HMAC-SHA1 con secret_key permanente) solo funciona para canales custom, no para canales WhatsApp ya conectados en Kommo.
