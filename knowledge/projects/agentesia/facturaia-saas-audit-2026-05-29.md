---
title: FacturaIA — Auditoría SaaS + Plan de implementación
date: 2026-05-29
source: claude-code audit (6 agentes + 2 agentes revisión)
tags: [facturaia, saas, billing, stripe, seguridad, admin, planes, módulos]
---

# FacturaIA — Auditoría SaaS completa + Plan de implementación

Auditoría realizada el 2026-05-29 sobre el sistema de planes, módulos, pagos y restricciones de TuFacturaIA.

---

## RESUMEN EJECUTIVO

La arquitectura de planes/módulos está **bien diseñada en BD y frontend** pero la capa de enforcement en API tiene agujeros de seguridad reales y monetización que sangra:

- Quotas declaradas en BD pero no aplicadas en ninguna ruta
- OCR sin feature gate en 2 de 3 canales (email y upload)
- Sistema de planes base sin Stripe detrás
- 5 endpoints de módulos sin ninguna validación de plan

---

## HALLAZGOS POR SEVERIDAD

### P0 — Críticos (monetización + seguridad activa)

| # | Problema | Archivo | Impacto |
|---|---|---|---|
| 1 | `/api/upload` sin `orgHasFeature('ocr')` | `src/app/api/upload/route.ts` | Starter accede a OCR gratis, consume LLM credits |
| 2 | `/api/email/poll` sin feature gate | `src/app/api/email/poll/route.ts` | Igual que arriba por canal email |
| 3 | `/api/modules/[id]` GET/PATCH sin feature gate | `src/app/api/modules/[id]/route.ts` | Starter lee/escribe config de módulos Pro |
| 4 | `/api/modules/[id]/metrics` y `/activity` sin gate | Misma ruta | Starter ve métricas de módulos que no tiene |
| 5 | `plan_limits.ocr_mes` (20/200/∞) definido pero **nadie lo consulta** | DB + todas las rutas de ingesta | Quotas decorativas, sin enforcement |
| 6 | Precios hardcoded en UI (19€/49€) vs DB (29€/79€) | `src/components/settings/plan-billing.tsx` | Usuario ve precio incorrecto |

### P1 — Altos (Stripe + seguridad infraestructura)

| # | Problema | Archivo | Impacto |
|---|---|---|---|
| 7 | `invoice.payment_failed` solo hace log (TODO en código) | `src/app/api/billing/stripe-webhook/route.ts:282` | Pago falla, nadie se entera, usuario sigue activo días |
| 8 | Sin `customer.subscription.updated` handler | Mismo archivo | Cambios de plan en Stripe no se reflejan en BD |
| 9 | Sin `invoice.payment_succeeded` handler | Mismo | Fallos de pago nunca se limpian en BD |
| 10 | Plan base sin Stripe (`organizations.plan` se edita manualmente en BD) | Sin endpoint | Sin renovación automática, sin churn detectado |
| 11 | Auth rutas internas: solo `x-service-key` header sin firma ni timestamp | `src/lib/voice/auth.ts`, `email/poll` | Key filtrada = acceso total a rutas internas |
| 12 | Cookie de impersonación sin firmar con HMAC | `src/lib/supabase/middleware.ts:43-80` | XSS puede redirigir superadmin a org arbitraria |
| 13 | `active → suspended` no permitido en máquina de estados | `change_billing_status` RPC (mig 004) | Cron de suspensión por pago fallido no puede ejecutarse |

### P2 — Medios (UX + observabilidad)

| # | Problema | Impacto |
|---|---|---|
| 14 | Read-only mode sin indicador persistente (solo banner que desaparece) | Usuario no sabe por qué no puede editar |
| 15 | Features ocultas del sidebar = no descubribles | Usuario no sabe que existen módulos de plan superior |
| 16 | Trial countdown empieza tarde (día 3) | Usuario sorprendido cuando expira |
| 17 | Add-on purchase sin confirmación ni pantalla de éxito | Usuario no sabe si compró |
| 18 | `invoice.payment_failed` no tiene grace period propio (espera a que Stripe cancele) | Usuario sin aviso 3-5 días hasta cancelación |
| 19 | Tab "Actividad" en admin org → "Próximamente" | Admin no puede ver historial |
| 20 | Sin MRR dashboard | Cero visibilidad financiera |

### P3 — Menores (deuda técnica + schema)

| # | Problema |
|---|---|
| 21 | `org_module_config` es JSONB sin constraint de DB (validación solo en código) |
| 22 | `billing_cycle_at` mutable sin audit trail |
| 23 | `fiscal_canceled_at` sin campo reason |
| 24 | `grace_days` se lee en cada request desde `plans` (O(1) extra query evitable) |
| 25 | `plans` no tiene `precio_anual` ni `activo` (o no está expuesto en API) |
| 26 | Admin panel: módulos sin kill switch global ni `coming_soon` flag a nivel módulo |
| 27 | Admin panel: sin audit log visible (tablas existen, UI no existe) |

---

## PLAN DE IMPLEMENTACIÓN

### Fase 1 — P0: Feature gating + quotas (esta semana)

#### 1.1 Helper `checkFeatureGate`

**Nuevo archivo**: `src/lib/api/feature-gate.ts`

```typescript
export async function checkFeatureGate(
  orgId: string | null,
  featureId: string,
): Promise<{ allowed: boolean; response?: NextResponse }> {
  if (!featureId) return { allowed: true }
  if (!orgId) return { allowed: false, response: NextResponse.json(
    { error: 'feature_unavailable', feature: featureId, reason: 'no_org' }, { status: 403 }
  )}
  const has = await orgHasFeature(orgId, featureId)
  if (!has) return { allowed: false, response: NextResponse.json(
    { error: 'feature_unavailable', feature: featureId, reason: 'plan_limit' }, { status: 403 }
  )}
  return { allowed: true }
}
```

Response canónica: `{ "error": "feature_unavailable", "feature": "ocr", "reason": "plan_limit" }` → HTTP 403

**Modificar** `src/lib/api/with-api-auth.ts`:
- Añadir `requireFeature?: string` a `WithApiAuthOptions`
- Ejecutar gate DESPUÉS de resolver `orgId`, ANTES de rate limit (superadmin lo saltea igual que `requireWrite`)

**Integrar en**:
- `api/upload/route.ts` → `requireFeature: 'ocr'`
- `api/modules/[id]/route.ts` → gate dinámico: `checkFeatureGate(orgId, id)` tras resolver el módulo
- `api/email/poll/route.ts` → dentro del loop de conexiones: gate por `conn.org_id` antes de `processAttachments`

#### 1.2 Helper `checkOrgQuota`

**Nuevo archivo**: `src/lib/billing/quota.ts`

```typescript
export async function checkOrgQuota(orgId: string, quotaKey: QuotaKey): Promise<QuotaCheckResult>
// 1. Lee plan de la org
// 2. Límite efectivo: org_limits override > plan_limits del plan
// 3. Uso actual via RPC get_org_usage (ya existe en BD)
// 4. Si used >= limit → 429 con headers X-RateLimit-Limit/Remaining/Reset + Retry-After
```

**Migration 181** (antes de activar): índice en `bandeja_ingesta(org_id, created_at)` para no hacer seq scan en el COUNT mensual.

**Integrar en**:
- `api/upload/route.ts` → ANTES del file scan (operación costosa)
- `api/internal/whatsapp/ingesta/route.ts` → tras resolver org
- `api/email/poll/route.ts` → dentro del loop, antes de `processAttachments`

Headers en 429: `X-RateLimit-Limit`, `X-RateLimit-Remaining: 0`, `X-RateLimit-Reset` (unix timestamp inicio mes siguiente), `Retry-After` (segundos).

#### 1.3 Fix precios en UI

`src/components/settings/plan-billing.tsx` → leer precios de DB (`supabase.from('plans').select('id,precio_mes,precio_anual,...')`) en lugar de las constantes hardcodeadas 19€/49€.

#### Orden fase 1

1. `feature-gate.ts` + tests
2. `quota.ts` + tests
3. Migration 181 (índice)
4. Integrar en upload → email/poll → modules
5. Fix precios UI
6. Smoke: org Starter + upload → 403; 21 uploads → 429

---

### Fase 2 — P1: Stripe completo (próximas 2 semanas)

#### 2.1 Schema changes (migrations 182-185)

```sql
-- 182: billing payment failed
ALTER TABLE organizations ADD COLUMN payment_failed_at TIMESTAMPTZ;
ALTER TABLE organizations ADD COLUMN payment_failed_invoice_id TEXT;
ALTER TABLE organizations ADD COLUMN payment_grace_until TIMESTAMPTZ;
ALTER TABLE organizations ADD COLUMN payment_failed_count SMALLINT DEFAULT 0;

-- 183: máquina de estados — añadir active→suspended
-- (actualizar change_billing_status RPC para permitir esta transición)

-- 184: cancel scheduling
ALTER TABLE organizations ADD COLUMN billing_cancel_scheduled_at TIMESTAMPTZ;

-- 185: base subscription ID
ALTER TABLE organizations ADD COLUMN base_stripe_subscription_id TEXT;
```

#### 2.2 `invoice.payment_failed` completo

**Nuevo archivo**: `src/lib/billing/payment-failed.ts`

```typescript
export async function handlePaymentFailed({ orgId, invoiceId }) {
  // 1. Escribe payment_failed_at, payment_grace_until = now() + 72h
  // 2. Inserta en email_outbox (patrón existente): template 'payment_failed'
}

export async function handlePaymentSucceeded({ orgId }) {
  // Limpia payment_failed_at, payment_grace_until, payment_failed_count → 0
}
```

**Cron nuevo**: `src/app/api/internal/billing/suspend-overdue/route.ts`
- GET con `x-service-key`
- Query: orgs con `payment_grace_until < now()` AND `billing_status='active'`
- Para cada una: `change_billing_status(org_id, 'suspended')`
- Schedule en n8n: cada hora

**Webhook handler** (`stripe-webhook/route.ts`):
- Reemplazar case `invoice.payment_failed`: llamar `handlePaymentFailed`
- Añadir case `invoice.payment_succeeded`: llamar `handlePaymentSucceeded`

#### 2.3 `customer.subscription.updated` handler

Mapeo `price_id → plan` desde env vars (`STRIPE_PRICE_ID_STARTER_MENSUAL`, etc.).

Cuando llega el evento:
- Si hay cambio de plan → actualizar `organizations.plan`
- Si downgrade → llamar `downgradeFeaturesToPlan(orgId, newPlan)`
- Si `cancel_at_period_end=true` → marcar `billing_cancel_scheduled_at`

**Nuevo archivo**: `src/lib/billing/downgrade.ts`
- Lee `plan_features` del nuevo plan
- Para features activas en `org_features` que no están en el nuevo plan → `enabled=false`
- No borra: mantiene historial, simplifica rollback

#### 2.4 `POST /api/billing/change-plan`

**Nuevo archivo**: `src/app/api/billing/change-plan/route.ts`
- `withApiAuth` con `requireWrite: 'billing'`, rate limit 5
- Body: `{ plan: 'starter'|'pro'|'enterprise', billing: 'mensual'|'anual' }`
- Llama Stripe subscription update con proration inmediata
- Actualiza `organizations.plan` (optimista, webhook también lo hace → idempotente)
- Si downgrade: llama `downgradeFeaturesToPlan`
- Edge case: si hay add-on activo fuera del nuevo plan, cancelar también la suscripción Stripe del add-on

**Env vars necesarias**:
```
STRIPE_PRICE_ID_STARTER_MENSUAL=price_xxx
STRIPE_PRICE_ID_STARTER_ANUAL=price_xxx
STRIPE_PRICE_ID_PRO_MENSUAL=price_xxx
STRIPE_PRICE_ID_PRO_ANUAL=price_xxx
STRIPE_PRICE_ID_ENTERPRISE_MENSUAL=price_xxx
STRIPE_PRICE_ID_ENTERPRISE_ANUAL=price_xxx
```

#### 2.5 Hardening auth rutas internas

**Nuevo archivo**: `src/lib/internal/auth.ts`

Header nuevo: `X-Service-Signature: t=<unix>,v1=<hmac_sha256_hex>`
Payload firmado: `<t>.<sha256_hex_del_body>`
Tolerancia: ±5 min (igual que webhook Stripe)

Estrategia de migración sin downtime:
- `FACTURAIA_SIGNING_SECRET` = nuevo secret HMAC (env nueva)
- `SIGNING_LEGACY_UNTIL` = fecha de corte (30 días desde deploy)
- Durante el período: acepta AMBOS formatos, logea warning si usa legacy
- Después de la fecha: rechaza legacy

**Env vars nuevas**:
```
FACTURAIA_SIGNING_SECRET=<openssl rand -hex 32>
SIGNING_LEGACY_UNTIL=2026-07-01T00:00:00Z
```

n8n genera la firma en un Code node antes del HTTP Request. Ver `buildSignatureHeader()` en `auth.ts`.

**Rutas a migrar**: `api/email/poll`, `api/internal/whatsapp/ingesta`, `api/internal/billing/suspend-overdue` y demás en `api/internal/*`.

#### 2.6 Fix máquina de estados

Migration 183 actualiza `change_billing_status` RPC para permitir `active → suspended` (necesario para cron de payment grace). Añadir también `suspended → active` (reactivación tras pago).

#### Orden fase 2

1. Migration 182 (schema payment_failed)
2. Migration 183 (máquina de estados → active→suspended)
3. `payment-failed.ts` + webhook handlers (payment_failed + payment_succeeded)
4. Cron `suspend-overdue` + registrar en CRON_REGISTRY
5. Migration 184 (cancel_scheduled_at) + `customer.subscription.updated` handler
6. Migration 185 (base_stripe_subscription_id) + `change-plan` endpoint
7. `internal/auth.ts` + migrar rutas internas (empezar por las menos críticas)
8. Actualizar n8n workflows con nueva firma

---

### Fase 3 — Admin panel completo (2-4 semanas)

#### 3.1 Migrations schema para admin

```sql
-- 181_plans_pricing_extended.sql
ALTER TABLE plans ADD COLUMN IF NOT EXISTS precio_anual NUMERIC(10,2);
-- Verificar que activo y orden ya existen; añadir si no.

-- 182_modules_control_flags.sql
-- Leer primero /api/admin/modules/[id]/route.ts para confirmar nombre real de tabla.
-- Añadir: activo BOOLEAN, coming_soon BOOLEAN, beta BOOLEAN, plan_minimo TEXT, addon_price_global NUMERIC(10,2)

-- 184_audit_log_enrichment.sql
ALTER TABLE audit_log ADD COLUMN IF NOT EXISTS actor_email TEXT;
ALTER TABLE audit_log ADD COLUMN IF NOT EXISTS reason TEXT;
ALTER TABLE audit_log ADD COLUMN IF NOT EXISTS before_value JSONB;
ALTER TABLE audit_log ADD COLUMN IF NOT EXISTS after_value JSONB;
ALTER TABLE audit_log ADD COLUMN IF NOT EXISTS ip TEXT;
ALTER TABLE admin_audit_log ADD COLUMN IF NOT EXISTS org_id UUID REFERENCES organizations(id) ON DELETE SET NULL;
-- Vista unificada admin_audit_unified (UNION ALL de ambas tablas, solo lectura)
```

#### 3.2 Endpoints admin nuevos

```
# Planes
POST   /api/admin/plans                          crear plan
DELETE /api/admin/plans/[id]                     eliminar (guard: 0 orgs en ese plan)
POST   /api/admin/plans/[id]/duplicate           clonar plan + features + limits

# Módulos
PATCH  /api/admin/modules/[id]/kill-switch       { activo: bool, reason }
GET    /api/admin/modules/[id]/orgs              orgs con override activo en ese módulo (paginado)
GET    /api/admin/modules/[id]/audit             historial de cambios del módulo

# Billing por org
GET    /api/admin/orgs/[id]/billing              estado completo: fechas, add-ons activos, historial
PATCH  /api/admin/orgs/[id]/billing              { action: extend_trial|extend_grace|set_payment_failed|clear, days?, reason }

# Actividad por org
GET    /api/admin/orgs/[id]/activity             audit_log paginado de la org

# Monitoring
GET    /api/admin/monitoring/summary             trials_expiring, expired_long_ago, payment_failed, crons_health
GET    /api/admin/monitoring/stripe-events       stripe_events_processed últimos N
GET    /api/admin/monitoring/ocr-usage           top orgs por uso OCR del mes

# MRR
GET    /api/admin/mrr                            total, by_plan, by_month (6 meses)

# Audit log
GET    /api/admin/audit                          unified, ?page,admin_user_id,org_id,action,from,to
GET    /api/admin/audit/export                   CSV, mismos filtros, max 10k filas
```

#### 3.3 Endpoints admin modificados

```
PATCH /api/admin/plans/[id]
  Añadir: nombre, precio_anual, activo, orden
  Guard activo=false: org count check
  Añadir: audit log con before/after diff

GET /api/admin/orgs
  Añadir a SELECT: trial_ends_at, billing_cycle_at, stripe_customer_id
  Computed: days_left_trial
  Nuevo filtro: ?trial_expiring_days=3

PUT /api/admin/orgs/[id]/billing (existente)
  Añadir: reason al body → pasar a logAdminAction

PUT /api/admin/modules/[id] (existente)
  Añadir: activo, coming_soon, beta, plan_minimo, addon_price_global
```

#### 3.4 Reglas de negocio admin (no obviar)

- **Desactivar plan**: guard `COUNT(*) FROM organizations WHERE plan = id > 0` → 409 con N orgs bloqueantes
- **Kill switch módulo**: no elimina `org_features` — es capa encima. Al reactivar, todo vuelve sin reconfigurar
- **Extender trial**: solo si `billing_status = 'trial'` → 409 si no
- **`coming_soon` + `beta`**: módulo visible pero no activable por el cliente. Admin puede activar por org manualmente para beta testers
- **Cambio de plan de org** (PATCH org): limpiar `org_features` source='plan' + recalcular según nuevo plan en transacción (no hacerlo en cliente)
- **Suspensión de org**: reason obligatoria en UI (no duro en API pero validar en frontend)
- **Audit log before/after**: actualizar `logAdminAction` en `src/lib/admin.ts` para aceptar `{ before, after, reason, ip, actorEmail }` → escribirlos en las nuevas columnas

#### 3.5 Cron de alertas diarias

Añadir a CRON_REGISTRY: `daily-admin-alert`
- Schedule: `0 8 * * *` (8:00 UTC)
- Queries: trials expirando <3d + expiradas >7d + payment_failed activos + crons con error
- Si hay items → email a superadmin con resumen (usar SMTP existente `info@agentesia.madrid`)
- También postear a #pro-facturaia si hay alertas críticas (via Slack MCP)

#### 3.6 UX críticos a arreglar (en paralelo)

- **Indicador persistente de read-only**: badge en header/status bar, no solo banner (desaparece al navegar)
- **Sidebar**: mostrar features no incluidas en gris con chip de plan. No ocultar — ocultar = no descubribles
- **Trial urgency desde día 7** (no día 3)
- **Add-on purchase**: modal de confirmación + pantalla de éxito explícita
- **Botón "Nueva factura" disabled**: tooltip en click, no solo hover (invisible en móvil)
- **BillingBanner copy**: diferenciar "expirado" vs "suspendido" vs "cancelado" con copy y CTA específico por estado

---

## ARQUITECTURA DE SEGURIDAD FINAL

### Feature gate layer (de mayor a menor prioridad)

```
1. features.activo = false → bloqueado globalmente (kill switch)
2. org_features.enabled override → override explícito por org
3. plan_features.enabled → valor del plan de la org
4. fallback → false
```

La función SQL `org_has_feature(p_org_id, p_feature_id)` ya implementa esta lógica. El problema era que no se llamaba desde las API routes. Con los cambios de Fase 1, todas las rutas la llaman.

### Quota layer

```
1. check_ingesta_rate_limit (100/24h) — burst protection, ya existe
2. checkOrgQuota('ocr_mes') — monthly plan limit, nuevo
3. Rate limit por endpoint via withApiAuth — anti-abuse
```

### Auth layer rutas internas

```
Antes: x-service-key (static string comparison)
Después: X-Service-Signature: t=<unix>,v1=<hmac> (time-bound, anti-replay)
Transición: 30 días con ambos formatos aceptados
```

---

## ESTADO DE TESTS REQUERIDOS

### Tests a crear (vitest)

- `src/lib/api/__tests__/feature-gate.test.ts` — 5 casos
- `src/lib/billing/__tests__/quota.test.ts` — 9 casos
- `src/lib/internal/__tests__/auth.test.ts` — 8 casos
- `src/lib/billing/__tests__/payment-failed.test.ts` — 4 casos
- `src/lib/billing/__tests__/downgrade.test.ts` — 3 casos

### Smokes manuales clave

1. Org Starter + `POST /api/upload` → 403 `feature_unavailable`
2. Org Starter + 21 uploads (uno por uno) → el 21 devuelve 429 con headers X-RateLimit-*
3. `stripe trigger invoice.payment_failed` → verificar `payment_failed_at` en organizations
4. `stripe trigger invoice.payment_succeeded` → verificar que se limpia
5. `POST /api/billing/change-plan { plan: 'starter' }` con org Pro → verificar features Pro desactivadas
6. `GET /api/admin/audit?org_id=<id>` → devuelve historial de cambios de la org

---

## DEPENDENCIAS ENTRE TAREAS

```
Feature gate (1.1) → no bloquea nada, puede ir ya
Quota enforcement (1.2) → no bloquea nada, puede ir ya
Migration 182 → bloquea payment_failed handler (2.2) y cron suspend-overdue (2.3)
Migration 183 → bloquea cron suspend-overdue (necesita active→suspended)
Migration 184 → bloquea audit log UI (3.6)
internal/auth.ts → no bloquea nada, puede ir ya pero coordinación con n8n
change-plan endpoint → requiere migration 185 + base_stripe_subscription_id en checkout base
Admin panel secciones → independientes entre sí (cada sección es un mini-sprint)
```

---

## ARCHIVOS CLAVE DEL PROYECTO

- `src/lib/billing.ts` — state machine de billing (getOrgBilling, lazy transitions)
- `src/lib/billing/fiscal-checkout.ts` — Stripe addon fiscal
- `src/app/api/billing/stripe-webhook/route.ts` — webhook handler
- `src/lib/modules/catalog.ts` — catálogo de módulos (SINGLE SOURCE OF TRUTH)
- `src/lib/features.ts` — orgHasFeature y derivados
- `src/lib/api/with-api-auth.ts` — wrapper de autenticación API
- `src/lib/voice/auth.ts` — requireServiceKey (a migrar)
- `src/lib/admin.ts` — logAdminAction (ampliar con before/after/reason)
- `supabase/migrations/004_admin_feature_flags.sql` — org_has_feature RPC + schema planes

---

## REFERENCIAS

- [[facturaia]] — Hub maestro del proyecto
- Auditoría generada por 6 agentes especializados + 2 agentes de revisión en sesión 2026-05-29
- Código base: `/Users/manueldelmonte/facturaia`
