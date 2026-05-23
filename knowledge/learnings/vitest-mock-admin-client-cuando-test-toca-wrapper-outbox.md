---
title: Vitest — mock @/lib/admin cuando el test toca un wrapper con INSERT outbox previo
date: 2026-05-23
source: cierre P0 — 12 tests email rotos tras sprint observabilidad mig 152
tags: [vitest, mocks, email, outbox, supabase]
---

## Síntoma

Tests legacy de `change-email`, `colleague-email`, `team-invite-email` que mockean `nodemailer` + `fetch` (Resend) fallan tras el refactor del sprint observabilidad con `errorCode: 'admin_client_init_failed'`. El wrapper `src/lib/email/send.ts` (mig 152) introdujo una capa nueva: INSERT `email_log` status=pending **antes** del provider real.

## Causa

`sendEmail()` ahora:

1. `createAdminClient()` — requiere `SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY` en envs.
2. `admin.from('email_log').insert(...).select('id').single()` — INSERT outbox.
3. Llamar Resend / SMTP (esto sí lo mockean los tests).
4. UPDATE `email_log` con `resend_id` + status sent/failed.

En vitest sin BD ni envs Supabase, paso 1 lanza y `sendEmail` devuelve `{ ok: false, error_code: 'admin_client_init_failed' }` sin tocar el mock de fetch/nodemailer. Los `expect(res.ok).toBe(true)` revientan.

## Solución (patrón reutilizable)

Mock chainable de `@/lib/admin` con stubs que resuelven INSERT/UPDATE/SELECT sin BD:

```ts
vi.mock('@/lib/admin', () => ({
  createAdminClient: () => ({
    from: () => ({
      insert: () => ({
        select: () => ({
          single: async () => ({ data: { id: 'outbox-mock-1' }, error: null }),
        }),
      }),
      update: () => ({ eq: async () => ({ data: null, error: null }) }),
      select: () => ({
        gte: () => ({
          contains: () => ({
            limit: async () => ({ data: [], error: null }),
          }),
        }),
      }),
    }),
  }),
}))
```

Con esto:
- INSERT pending devuelve un id sintético — `sendEmail` sigue al paso 2 (provider).
- Los assertions de fetch/nodemailer originales del test siguen siendo válidos.
- UPDATE final es no-op silencioso (no se mide en los tests).
- La idempotency check (`select().gte().contains().limit()`) devuelve array vacío — nunca devuelve el cached, siempre re-envía.

## Cuándo usarlo

Cualquier test futuro que toque un helper que internamente llame a `sendEmail` (otp, factura_enviada, presupuesto_enviado, team_invite, colleague, etc.) necesita este mock. Sin él, el test falla con `admin_client_init_failed` aunque el provider esté correctamente mockeado.

## Alternativa rechazada

Mockear directamente `sendEmail` con `vi.mock('@/lib/email/send', () => ({ sendEmail: vi.fn().mockResolvedValue({ ok: true, ... }) }))`. Funciona pero pierde la cobertura del comportamiento del provider (assertions sobre body de fetch, sendMail args). Mejor mockear la capa BD y dejar el wrapper ejercitar Resend/SMTP de verdad.

## Cross-ref

Wrapper en `src/lib/email/send.ts`. Mig 152 `email_log` columnas ampliadas + tabla `email_log_events`. Sprint observabilidad cierre 2026-05-23 (Histórico de hitos).
