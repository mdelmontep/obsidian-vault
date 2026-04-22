---
title: tecnocloud — whatsapp facturaia pendiente
date: 2026-04-22
source: claude-code-session
tags: [tecnocloud, facturaia, whatsapp, pendiente]
---

Intentamos configurar WhatsApp para la org Tecnocloud en FacturaIA. El schema Zod está arreglado (acepta `telefono` y `settings`), pero falta:

1. Obtener el `phone_number_id` de Meta Business Suite para el número de Tecnocloud
2. Guardarlo en `organizations.settings.whatsapp.phone_number_id` (org id: `8714c897-8e2e-472f-aa40-9f591510c88c`)
3. Configurar webhook override por número en Meta (patrón: `POST graph.facebook.com/v22.0/{phone_number_id}` con `webhook_configuration`)
4. Verificar que el workflow receptor n8n (`zYcHHa8jWXB6dY5i`) matchea la org por `phone_number_id`

La org existe en Supabase pero tiene `settings: {}` — completamente vacío.
