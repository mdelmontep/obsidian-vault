---
title: UPSERT sombra por id remoto, no por id local — múltiples paths convergen sin duplicar
date: 2026-05-01
source: claude-code-session
tags: [supabase, idempotency, sync, sombras, agency-portal]
---

Cuando un sistema local tiene "sombra" de un recurso remoto y varios paths pueden crearla (webhook entrante, sync periódico, auto-emit, manual), el UPSERT debe usar el id remoto como ancla, NO el id local.

- mal: `upsert({...}, { onConflict: 'id' })` — el id local solo lo conoce un path
- mal: select por remote_id + INSERT/UPDATE — race condition entre paths
- bien: `upsert({agency_id, remote_id, num, [fk_local]}, { onConflict: 'remote_id' })`

El remote_id existe en TODOS los paths. Si webhook llega primero, sombra ya tiene remote_id y el auto-emit upserta sobre la misma fila añadiendo el FK local.

Bug real: agency-portal `auto-emit.ts` y `emit-from-stripe.ts` enlazaban por `id`; si webhook llegaba antes, auto-emit creaba duplicada. Fix: UPSERT por remote_id.

Aplica a syncs Stripe, n8n, integraciones B2B con sombras locales.
