---
title: ADR-026 — Sistema SaaS: feature gating, Stripe completo, HMAC interno
date: 2026-05-30
status: implemented (rama feat/saas-fase2-stripe-completo, PRs #91 #92, pendiente merge)
deciders: Manuel Del Monte
tags: [adr, facturaia, saas, billing, stripe, hmac, auth, feature-gates]
related: [[facturaia-saas-audit-2026-05-29]] [[migracion-auth-sin-downtime-con-signing-legacy-until]] [[env-fecha-mal-formada-fail-closed-no-fail-open]] [[migrar-auth-wrapper-default-vs-handler-por-handler]] [[test-mocks-rename-import-path-no-rename-import]] [[date-trunc-en-where-no-sargable-aunque-haya-indice]]
---

# ADR-026 — Sistema SaaS de TuFacturaIA: feature gating, Stripe completo, HMAC interno

## Contexto

Auditoría completa 2026-05-29 (6 agentes especializados + 2 de revisión) detectó que el sistema de planes/módulos/pagos tenía la arquitectura BD bien diseñada pero la capa de enforcement vacía:

- **5 endpoints** sin feature gate (`/api/upload`, `/api/email/poll`, `/api/modules/[id]` GET/PATCH/metrics/activity) → cualquier user accedía a features de plan superior.
- **Quotas en BD pero nadie las consulta**: `plan_limits.ocr_mes` (20/200/∞) era decorativo.
- **Webhook Stripe incompleto**: `invoice.payment_failed` era TODO log-only, sin `payment_succeeded`, sin `customer.subscription.updated`. Stripe cancelaba después de días sin que nadie se enterara.
- **Plan base sin Stripe self-service**: `organizations.plan` se editaba a mano.
- **Auth rutas internas con secret estático**: `x-service-key` sin HMAC ni timestamp.
- **Precios hardcoded** en UI (19€/49€) vs DB (29€/79€).

Plan original detallado en [[facturaia-saas-audit-2026-05-29]].

## Decisión

5 commits sobre `feat/saas-fase2-stripe-completo`:

| Commit | Fase | Alcance |
|---|---|---|
| `f3d1245` | 1 | Feature gates + quotas (P0) |
| `36b7166` | 2 | Stripe completo + HMAC (P1) |
| `4614b75` | hardening | Audit follow-up 4 agentes (8 fixes) |
| `5bca0d9` | 2.5 | `withCronTracking` default HMAC + handler extraído + 4 rutas críticas |
| `45ad780` | 2.6 | 22 rutas internas restantes a HMAC |
| `+ 1` final | hardening 2 | Audit cross-PR final (5 fixes) |

### Pilares arquitectónicos

**1. Feature gating layered**
- BD owner: `org_has_feature(org_id, feature_id)` RPC (mig 004). Override de `org_features` > default de `plan_features`.
- API gate: `src/lib/api/feature-gate.ts` (`checkFeatureGate`) + `requireFeature` opt en `withApiAuth`.
- Quota gate: `src/lib/billing/quota.ts` (`checkOrgQuota`). Override `org_limits` > `plan_limits` > RPC `get_org_usage` (mig 181 sargable — ver [[date-trunc-en-where-no-sargable-aunque-haya-indice]]).
- Race condition `quota` aceptada y documentada (acotada por `withApiAuth` rate-limit per-user).

**2. Stripe webhook completo**
- `invoice.payment_failed` → `handlePaymentFailed`: marca `payment_failed_at`, `payment_grace_until=now+72h`, escala `payment_failed_count`, envía email al propietario (idempotency key `payment_failed:<invoice_id>`). HTML con `escapeHtml` defense-in-depth.
- `invoice.payment_succeeded` → `handlePaymentSucceeded`: limpia los 4 campos.
- `customer.subscription.updated` → `handleSubscriptionUpdated` (extraído + 9 tests): mapeo `price_id→plan` desde env, downgrade calls `downgradeFeaturesToPlan` (preserva add-ons), `cancel_at_period_end` → `billing_cancel_scheduled_at`.
- Cron `suspend-overdue` (cada hora) suspende orgs con `grace_until < now`. **Re-check anti-race** entre SELECT y RPC para no suspender orgs que pagaron justo antes.

**3. `change-plan` self-service**
- `POST /api/billing/change-plan` con `withApiAuth + requireWrite:'billing'` (Resource nuevo TS-only) + rate 5/min.
- Guards: `billing_status === 'active'` (bloqueando trial/expired/suspended — fraude downgrade evitando deuda), cross-check `sub.customer === org.stripe_customer_id` (binding incorrecto), idempotencia no-op si ya en plan destino.
- Stripe REST manual con form-urlencoded + `parseStripeError` para no filtrar IDs de otras cuentas en errores 4xx/5xx.
- Add-on huérfano post-downgrade: **manual via UI dedicada**, NO automático — riesgo de pérdida de continuidad WORM AEAT 6 años.

**4. HMAC interno con migración sin downtime**
- `X-Service-Signature: t=<unix>,v1=<hmac_sha256_hex>`. Payload v2: `${t}.${method}.${path}${search}.${bodyHash}`. v1 legacy (sin method+path) aceptado como fallback hasta Fase 2.8 — eliminado tras todos los callers migren.
- Migración legacy `x-service-key` durante `SIGNING_LEGACY_UNTIL`. Fail-closed sobre fecha mal formada — ver [[env-fecha-mal-formada-fail-closed-no-fail-open]].
- Secretos independientes (`FACTURAIA_SIGNING_SECRET` ≠ `FACTURAIA_SERVICE_KEY`) — compromiso de uno no autoriza el otro.
- Default `withCronTracking` migrado a HMAC, ~30 crons pasan de golpe — ver [[migrar-auth-wrapper-default-vs-handler-por-handler]].
- 22 rutas no-cron migradas manualmente con body firmado (anti-tampering). 10 tests actualizaron sus mocks — ver [[test-mocks-rename-import-path-no-rename-import]].

### Decisiones contraintuitivas (justificadas)

| Decisión | Razón |
|---|---|
| Add-on huérfano post-downgrade NO se cancela automáticamente | Continuidad WORM AEAT 6 años — cancelar mid-period pierde acceso a docs fiscales sellados eIDAS. Plan original §2.4 lo proponía auto; rebajado tras audit. |
| Race quota optimista aceptada (1-2 unidades overshoot) | Acotada por rate-limit per-user + idempotencia sha256 + coste atomic check >> ganancia. |
| HMAC v1 compat-fallback en lugar de cutover duro | n8n workflows externos firman con generador propio — migración progresiva, no big-bang. |
| `Resource = 'billing'` solo en TS, no en SQL `user_can_write_in_org` | Endpoint usa service_role (bypass RLS); blanket 'all' cubre owner/admin. Replicar al SQL solo si futura tabla con RLS. |
| `change-plan` durante trial → 409 (no upgrade silencioso) | `proration_behavior=always_invoice` cobra inmediatamente, rompe expectativa de "14 días gratis". |
| HMAC GET firma sobre `""` + path | Body no aplica; el path en el payload bloquea replay horizontal con query distinto. |
| `downgradeFeaturesToPlan` no destructivo (`enabled=false`, no DELETE) | Re-upgrade restaura sin reconfigurar; respeta history. |
| Mig 181 reescribe `get_org_usage` sin índice nuevo | El índice `(org_id, created_at)` ya existía desde mig 004; el cuello era `date_trunc(col) =` no sargable. |

### Migraciones (181-186)

```
181  get_org_usage sargable (rewrite RPC, identidad lógica preservada TZ-invariante)
182  organizations.payment_failed_{at,invoice_id,count} + payment_grace_until + idx parcial
183  change_billing_status RPC + transiciones active↔suspended
184  organizations.billing_cancel_scheduled_at
185  organizations.base_stripe_subscription_id + UNIQUE parcial
186  idx_org_members_owner_active (parcial, lookup O(1) del propietario)
```

Todas idempotentes (`IF NOT EXISTS` / `CREATE OR REPLACE`). Sin tablas nuevas — la regla "RLS en misma migración" no aplica.

## Consecuencias

### Positivas

- 5 vulnerabilidades P0 cerradas + 8 P1.
- Plan starter ya NO puede usar OCR sin pagar; quotas activas.
- Webhook Stripe ya no pierde eventos `payment_failed`/`succeeded`.
- 33 rutas `/api/internal/*` con HMAC anti-tampering — solo 1 pendiente (`ocr-process`, rama paralela).
- `withCronTracking` default protege automáticamente cualquier cron futuro sin código adicional.
- Auditoría cross-PR con 4 agentes paralelos (security/correctness/architecture/perf) ratificó cero P0 reales post-implementación tras 2 rondas (audit Fase 2 + audit final cross-PR).

### Negativas / deuda

- Add-on huérfano post-downgrade requiere UI dedicada (Fase 2.7).
- 9 rutas `/api/voice/*` siguen con `requireServiceKey` legacy (tras `SIGNING_LEGACY_UNTIL` rompen; deben migrarse).
- `whatsapp/ocr-process` pendiente de migrar (rama paralela `feat/multidivisa-recibidas`).
- `requireFeatureResponse` legacy en 6 endpoints (`/conciliacion/*`, `/cashflow/*`) — convergencia con `checkFeatureGate` pendiente.
- Cookie `impersonate_org` sin HMAC firmar (P1-12 audit original, fuera de scope Fase 2).
- Tests E2E pendientes: 6 smokes en hub `00-home/facturaia.md`.
- UI `plan-billing.tsx` no cablea aún `POST /api/billing/change-plan` — endpoint listo pero sin invocador.

### Operacional pre-merge

Envs a setear en Dokploy antes del cutover:
```
STRIPE_PRICE_ID_{STARTER,PRO,ENTERPRISE}_{MENSUAL,ANUAL}   # 6 vars
FACTURAIA_SIGNING_SECRET=$(openssl rand -hex 32)
SIGNING_LEGACY_UNTIL=2026-07-01T00:00:00Z                   # 30 días desde deploy
```

Webhook Stripe — suscribir a:
- `invoice.payment_succeeded`
- `customer.subscription.updated`

`supabase db push --linked` desde main limpio para aplicar 181-186.

## Alternativas descartadas

- **Cancelación automática del add-on en downgrade**: WORM AEAT pesa más.
- **HMAC sin path firmado**: replay horizontal real demostrado en audit → v2 incluye path.
- **Atomicidad quota via RPC con SELECT FOR UPDATE**: rate-limit per-user es suficiente, evita overhead.
- **Migración handler-por-handler de los ~30 crons**: cambiar default del wrapper es más eficiente.
- **Crear un `Resource='billing'` en SQL**: sin RLS asociada, redundante. Mantenido TS-only documentado.
- **Stripe SDK oficial**: el repo ya replica HMAC manual (igual que fiscal-checkout). Mantener consistencia.

## Futuro (Fase 2.7+)

1. UI `plan-billing.tsx` cablea `POST /api/billing/change-plan` con confirm modal.
2. Migrar 9 rutas `/api/voice/*` a HMAC.
3. Borrar `src/lib/voice/auth.ts` legacy.
4. Code nodes n8n con `buildSignatureHeader({body, secret, method, pathWithSearch})`.
5. UI dedicada "¿cancelar también add-on fiscal?" en downgrade.
6. Endpoint trial upgrade dedicado.
7. Fase 2.8: eliminar v1 fallback en HMAC verifier.
8. Fase 3 admin panel: 19 endpoints nuevos (extend_trial, suspend, MRR dashboard, audit log UI, kill switches por módulo).

## Aprendizajes destacados al vault

- [[date-trunc-en-where-no-sargable-aunque-haya-indice]]
- [[migracion-auth-sin-downtime-con-signing-legacy-until]]
- [[env-fecha-mal-formada-fail-closed-no-fail-open]]
- [[migrar-auth-wrapper-default-vs-handler-por-handler]]
- [[test-mocks-rename-import-path-no-rename-import]]
