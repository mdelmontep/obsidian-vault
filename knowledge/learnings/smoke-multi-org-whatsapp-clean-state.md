---
title: smoke multi-org WhatsApp bot requiere limpiar 3 tablas + no abrir web
date: 2026-05-21
source: claude-code-session
tags: [facturaia, whatsapp, smoke, multi-org]
---

Para forzar el caso `reason='multi_org_pendiente'` del resolver
`/api/internal/whatsapp/resolve-context`:

1. `DELETE FROM whatsapp_org_selection WHERE user_id=X` (sticky bot, mig 125)
2. `UPDATE profiles SET active_org_id=NULL WHERE user_id=X` (sync web→bot)
3. Borrar memoria conversacional viva (`n8n_chat_histories` en Postgres
   local del n8n, NO Supabase — ver
   [[n8n-chat-histories-en-postgres-local-no-supabase]])

Gotcha clave: si abres `app.tufacturaia.com` entre el clean y el envío
WhatsApp, el endpoint `switch-org` repuebla sticky con `source='web_switch'`
TTL 24h automáticamente, y `profiles.active_org_id` también queda seteado.
La ventana entre clean y test WhatsApp tiene que ser cero-tráfico-web.

Alternativa para smoke sin clean destructivo: patch temporal del IF
`Tiene Sesion?` en workflow n8n → `rightValue: 0 → 999999999` (siempre
false) → fuerza entrada a `Buscar Org Texto` → revert tras smoke
(~30s ventana, afectación cero usuarios reales si tráfico esporádico).
