---
title: lookup profile cross-canal para audit DEBE scoping via org_members
date: 2026-05-05
source: claude-code-session
tags: [supabase, security, multi-tenant, audit]
---

Resolver identidad por dato externo (teléfono que envía WhatsApp, email del remitente) contra `profiles` SIN scoping a la org actual = vector cross-tenant impersonation latente. El mismo teléfono/email puede existir en otra org y se atribuiría al user equivocado.

Patrón seguro:

```ts
.from('profiles')
.select('user_id, full_name, org_members!inner(org_id, estado)')
.eq('phone', phoneRecibido)         // o .eq('email', senderEmail)
.eq('org_members.org_id', orgId)
.eq('org_members.estado', 'activo')
.maybeSingle()
```

Si no hay match: NUNCA fallback a profile sin scoping. Mejor guardar el dato crudo (`actor_name=phone`, `actor_email=sender`) y dejar `user_id=null`.

Aplica a: webhook receivers, agentes voz/email, cualquier audit donde resuelves "quién creó esto" desde dato externo. En FacturaIA migration 039 lo apliqué para `created_by_user_id` en `/api/voice/generate` y `email/process-attachments`.
