---
title: helper con client inyectado por parámetro — moverlo dentro si ningún caller lo reutiliza
date: 2026-07-05
source: claude-code-session
tags: [arquitectura, testing, facturaia, port-pattern]
---

Un helper de dominio (`createOrGetPaymentLink(admin, orgId, facturaId)`) recibía el
cliente Supabase admin por parámetro — patrón DI legítimo para testear sin mockear
el módulo entero. Pero los 3 callers hacían `createAdminClient()` SOLO para esa
llamada, sin reutilizarlo para nada más. Cuando 2 de esos callers estaban migrados
a un patrón "port" con un gate que prohíbe `createAdminClient` directo (evita el
seam que el port vino a eliminar), la DI del helper forzaba a reintroducir
justo ese import — rompiendo el gate por una razón ajena al propio port.

**Fix**: antes de asumir que el parámetro DI es intocable, grep TODOS los callers.
Si ninguno reutiliza el client para otra cosa, mover `createAdminClient()` dentro
del helper (mismo patrón que otros servicios de dominio invocados directo) y
adaptar su test a mockear el módulo `@/lib/admin`, no a inyectar el objeto.
Simplifica los callers Y respeta el gate sin tocar su semántica.
