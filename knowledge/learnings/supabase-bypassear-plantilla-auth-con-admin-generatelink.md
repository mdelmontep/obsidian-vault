---
title: bypassear plantillas auth supabase usando admin.generateLink + envío propio
date: 2026-05-26
source: claude-code-session
tags: [supabase, auth, email, resend]
---

Cuando la plantilla default Supabase es spam-prone (inglés, sin branding, Gmail banner rojo "External / Spam"), no luchar contra el editor del Dashboard. Patrón:

1. Endpoint server propio con service-role
2. `supabase.auth.admin.generateLink({ type: 'recovery'|'invite'|'magiclink'|'signup', email, options: { redirectTo } })`
3. Devuelve `action_link` SIN disparar SMTP de Supabase
4. Tu app envía vía Resend con plantilla custom castellano/branded + outbox loggeado + anti-enum (siempre 200)

Beneficios: SPF/DKIM/DMARC alineados con tu dominio, plantilla versionada en Git, rate-limit propio. Aplica también a magic-link/invite/change-email. Caveat: si fallas el fetch a Resend el user no recibe nada — Supabase ya no es failsafe.

**`signup` (confirmación de alta)**: es el que más se olvida al migrar (en FacturaIA quedó en Supabase hasta 2026-06-15, PR #256). `generateLink({type:'signup', email, password})` CREA el user (unconfirmed) y devuelve el link → reemplaza a `auth.signUp` client-side por completo. Síntoma del email integrado de Supabase: lento + rate-limit estricto → **el reintento con el mismo email deja de enviar**. Para reenviar a un unconfirmed: bórralo (no tiene org sin confirmar) y regenera. Ver [[supabase-createuser-race-trigger-handle-new-user]].
