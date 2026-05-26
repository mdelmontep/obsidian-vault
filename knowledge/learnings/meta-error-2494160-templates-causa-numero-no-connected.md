---
title: meta error 2494160 "waba sin permiso plantillas" suele ser número no CONNECTED
date: 2026-05-26
source: claude-code-session
tags: [whatsapp, meta, templates, debugging]
---
`POST /{waba_id}/message_templates` → `error_subcode: 2494160 "no tiene permiso para
administrar plantillas"`. La intuición dice "permisos del token" pero NO.
Causa real (en orden de probabilidad):
1. WABA sin ningún número con `status: CONNECTED` en Cloud API.
2. Verificación de empresa del portfolio sin completar.
3. WABA no añadida como activo a la App.
Debug rápido: `GET /{phone_id}?fields=status,code_verification_status`. Si `DISCONNECTED`
o `NOT_VERIFIED` → arreglar antes de tocar templates. Mismo token vale tras conectar número.
Ver [[whatsapp-cloud-api-vs-business-app-numero-exclusivo]].
