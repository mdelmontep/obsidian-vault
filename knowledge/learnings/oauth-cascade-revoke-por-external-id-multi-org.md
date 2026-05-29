---
title: OAuth multi-org → cascada de revoke por external_id (sub Google)
date: 2026-05-29
source: claude-code-session
tags: [oauth, google, multi-org, integraciones]
---

Google emite **1 refresh_token por `(client_id, user, scopes)`**. Si user tiene N orgs en la app conectadas a la MISMA cuenta Google y revoca acceso desde `myaccount.google.com/permissions`, **TODAS las connections caen a la vez** (cada `integration_connections` row tiene su propio `refresh_token_enc` pero internamente apuntan al mismo grant revocado).

Si solo marcas `expired` la conexión que falló primero, las otras N-1 siguen reintentando cada tick del cron → logs spammeados + retries inútiles + UI muestra estado inconsistente.

Patrón: en `tokens.ts` cuando refresh devuelve `invalid_grant`, hacer SWEEP:

```ts
const { data: siblings } = await admin
  .from('integration_connections')
  .select('id')
  .eq('provider_slug', providerSlug)
  .eq('external_id', conn.external_id)  // sub Google, estable por user
  .neq('id', conn.id)
  .eq('status', 'active')
for (const s of siblings || []) {
  await updateConnectionStatus(s.id, 'expired', 'invalid_grant_cascade')
}
```

Worker outbox: además cancelar pending filas de TODAS las connections afectadas para no seguir intentando subir a Drive de una conexión revocada. Aplica también a cualquier provider con refresh tokens compartidos por scope (no solo Google).
