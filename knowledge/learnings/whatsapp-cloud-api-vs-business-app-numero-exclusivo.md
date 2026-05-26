---
title: whatsapp cloud api y app business móvil no coexisten en mismo número
date: 2026-05-26
source: claude-code-session
tags: [whatsapp, meta, cloud-api]
---
Un número WhatsApp vive en UN endpoint: app Business móvil O Cloud API. No ambos.
- Mientras esté en app móvil → Meta API ve `code_verification_status: NOT_VERIFIED` aunque
  esté verificado en la app (son sistemas separados).
- `POST /{phone_id}/register` devuelve `"Register endpoint is not available for SMB businesses"`
  → SMB tier debe registrar vía UI (Admin WhatsApp → Verificar).
- Coexistence API existe (2024+) pero solo vía Meta Tech Provider/BSP (Twilio, 360dialog…),
  no para devs directos.
- Migración: borrar cuenta de la app móvil (no logout) → exportar chats antes si interesan.
- Chatwoot no salva el constraint: usa Cloud API por debajo, requiere `status: CONNECTED`.
