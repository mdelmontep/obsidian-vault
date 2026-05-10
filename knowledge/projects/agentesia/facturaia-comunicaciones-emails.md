---
title: facturaia-comunicaciones-emails
date: 2026-05-10
source: sesión Claude Code (5 agentes review + síntesis)
tags: [facturaia, spec, comunicaciones, emails, resend, auth, plan]
---

# FacturaIA — Sistema de comunicaciones por email

Spec consolidada tras revisión por 5 agentes paralelos (codebase audit, security, architecture/scale, UX product, UI consistency). Reemplaza al plan original de 60 días / 8 sprints / ~30 tablas que duplicaba sistemas existentes.

Hub: [[facturaia]] · Decisiones cerradas en esta sesión, listas para ejecutar.

---

## 0. Decisiones clave tomadas

| Decisión | Resultado | Razón |
|---|---|---|
| Self-hosted vs Resend | **Resend** | Deliverability se compra, no se monta; Listmonk solo aporta cuando haya lista marketing real (no hoy) |
| Listmonk ahora | **No** | Sin lista de marketing, es complejidad sin valor. Reevaluar fase B cuando >500 leads |
| Stripe billing | **Separar** | Email y billing son sistemas independientes; mezclarlos triplica riesgo |
| Notif paralela vs reusar | **Reusar `notifications` (migr 050)** | Single source of truth. Email es CANAL, no sistema |
| Plan original 60 días | **Sustituido por 5 PRs** | Plan original sobre-ingenierizado (~60% recortado). 5 agentes coincidieron |
| Auth emails (signup/reset/magic) | **Supabase Auth + Custom SMTP Resend** | Síncronos al flujo, Supabase ya gestiona tokens; reescribir = vulnerabilidades |
| Dominio auth | **Separado: `auth.facturaia.agentesia.world`** | Aisla deliverability: complaint en marketing no tumba auth |
| Dominio transaccional | **`mail.facturaia.agentesia.world`** | Subdominio dedicado, no dominio raíz |
| Zod v3 vs v4 | **v4 instalado, sintaxis estilo v3** | Repo entero usa `z.string().email()`. v4 retrocompatible. Regla CLAUDE.md a actualizar |
| 4 agentes review + 1 UI | **5 agentes paralelos ejecutados** | Cada uno ángulo distinto, sin solape de edits (read-only) |

---

## 1. Síntesis de los 5 agentes (consenso fuerte)

### Auditoría codebase (estado actual)

- Última migración: **058** → siguiente libre **059**.
- **Email actual**: `nodemailer + SMTP` en `src/lib/email/send-factura.ts` y `send-presupuesto.ts`. Esto se reemplaza.
- **Notifications**: tabla `notifications` (migr 050) con `kind`, `category`, `severity`, `dedupe_key`, `payload jsonb` + `notification_reads` + triggers `trg_facturas_resolve_notifs`, `trg_bandeja_resolve_notifs`. Hook `useNotifications` (240 líneas, polling 60s + Realtime). Drawer en topbar.
- **Auth flows existentes**: `/login`, `/registro`, `/recuperar-contrasena`, `/nueva-contrasena`, `/verificar-email`, `/invitacion`. Supabase Auth nativo, sin templates custom en código.
- **Sistema módulos IA**: `module_metadata` (045), `module_events`, `org_module_config`, `ai_module_suggestions`. Paths `/admin/modules`, `/agentes`, `/settings/modulos`. Modal 5 tabs (Cómo funciona / Métricas / Actividad / Config / IA).
- **Outbox transaccional ya existe** para webhooks salientes (PR-A3 en prod). `outbox_events` + dispatcher `/api/internal/webhook-dispatcher`.
- **Stack**: Next 16.2.4, React 19.2.4, Supabase 2.103.3, Zod 4.3.6 (sintaxis v3 en código).
- **Helpers auth**: `withApiAuth` en `src/lib/api/with-api-auth.ts`. `withApiV1` para `/api/v1/*`. `requireAdmin` para `/api/admin/*`.

### Seguridad — P0 bloqueantes

1. **Custom sender domain phishing relay**: TXT challenge único per-org `_facturaia-challenge.<dominio>` con nonce 32 bytes. Blocklist TLDs reservados (.gov, .mil, .edu, .int) + dominios públicos (gmail.com, outlook.com, agentesia.madrid). Re-verificar TXT en cada cron (atacante puede borrarlo tras validar).
2. **RLS shape**: `email_log`, `email_queue`/outbox, `email_suppressions` globales, `domain_events`, `org_email_domains.dns_records`: **service_role only**. `notifications`, `notification_preferences`, overrides user: policy por `get_user_org_id()`.
3. **Prompt injection en IA**: features admin que leen contenido user (template assistant, bounce diagnoser) → wrapping XML `<user_template>...</user_template>` + system prompt anti-injection + tool calls deshabilitadas.
4. **Webhook replay**: HMAC con `crypto.timingSafeEqual`, reject si `|now - timestamp| > 5min`. Dedupe en `webhook_events_seen(provider, event_id PK)` con `INSERT...ON CONFLICT DO NOTHING` (NUNCA check-then-insert).

### Seguridad — P1 hardening

- Secrets rotation: `RESEND_API_KEY`, `RESEND_WEBHOOK_SECRET` solo en Dokploy env, redactor en logger.
- Auth emails via SMTP: confirmar `SITE_URL` estática (no derivada de request) → no host header injection. Tokens auth NO snapshot en `email_log.body_snapshot`.
- Impersonate-preview: render con datos **mock/anonimizados** del schema. Si admin necesita ver email real, leer `email_log` con `audit_log` row obligatorio.
- Open redirect: token unsubscribe = HMAC(`org_id|email|list_id`). Sanitizar URLs plantilla con allowlist `https:` + bloquear `javascript:`/`data:`.
- GDPR: derecho al olvido = `DELETE FROM email_log WHERE org_id=$1 AND to_email=$2` + tombstone en `email_suppressions` razón `gdpr_erasure`. Particionado solo para retención (drop partition >18m).
- Bounce loop: flag `is_system_notification=true`; si destino en suppressions, drop silencioso.
- DoS: rate limit `email_queue` INSERT — 1000/h/org enforced trigger BEFORE INSERT. Kill switch global `email_kill_switch`.

### Arquitectura — KEEP / QUITAR / AÑADIR

**KEEP fase 1**:
- Provider Resend con circuit breaker.
- **Outbox unificado**: extender `outbox_events` con `kind IN ('webhook','email')`. NO crear `email_queue` ni `domain_events` paralelos.
- 8 plantillas core React Email.
- Suppressions (global + per-org).
- Webhook Resend ingest → `email_log`.
- Extensión `notifications` con `channels jsonb` + nueva `notification_deliveries` (1:N por canal).
- Particionado `email_log` mensual con `pg_partman`.
- **List-Unsubscribe RFC 8058 (one-click)** — obligatorio Gmail/Yahoo desde 2024.
- Throttle per-org en dispatcher.
- Custom domain con verify cron 15min.

**QUITAR del plan original**:
- `notifications_inapp` paralela.
- `email_queue` separada.
- `domain_events` bus.
- 6 de 9 crons (consolidar 6 features IA en 1 cron nocturno único).
- 42 de 50 plantillas (bajo demanda).
- Failover SES fase 1.
- 3-capas resolver sin cache: usar **snapshot del template resuelto** en `email_log.template_resolved` al enqueue → 1 query al send.

**AÑADIR (huecos reales que faltan)**:
- Idempotency key caller→enqueue.
- Snapshot HTML capturado en cada delivery (lo que el user vio, no re-render).
- Dominio separado para Supabase Auth (`auth.facturaia.agentesia.world`).
- Ingest webhook Resend para auth emails (matchear por `to+message_id` y escribir `email_log` con `source='supabase_auth'`).
- Métricas Prometheus básicas (queue depth, age, failure rate).

### UX producto — estructura UI final

**Admin** `/admin/comunicaciones` con **3 tabs** (no 5):
- **Plantillas** (catálogo + editor + IA assist + test send) — auditoría como sub-tab del editor en drawer lateral.
- **Operaciones** (búsqueda emails + suppressions + reenvío + bounces + kill-switch) — 80% del uso real a las 3am.
- **Salud** (métricas + insights IA + dominios fallando) — fusiona métricas + insights + overview.

Per-org NO es pestaña: filtro `?org_id=` en Operaciones + override desde detalle plantilla. 10k orgs no caben en pestaña navegable.

**Cliente** módulo "Comunicaciones" en `/agentes` con tarjeta + página completa (NO modal 5-tabs porque editor necesita split-pane ancho que no cabe en modal):

`/settings/comunicaciones` con **3 tabs** (no 4):
- **Preferencias** (matriz evento × canal + digest).
- **Plantillas** (override slots, gated por plan).
- **Dominio + historial** (fusionado: dominio es setup one-shot, historial uso diario).

**In-app NO es pestaña** — es el drawer de campana ya existente con tabs internos `Todas | In-app | Email | WhatsApp`.

### UI consistencia — estética humana, no AI-made

**Referente único**: **Stripe**. Typography-first, jerarquía clara, marca sutil, CTA único, footer denso pero ordenado. NO Linear (denso, oscuro, dev-céntrico). NO Vercel (frío para fiscal/PyME).

**Layout email** (600px ancho):
- Fondo `#fafbfc`, contenido sobre `#fff`, border 1px `#e6e8ee` (sin shadow — Outlook lo rompe).
- Header: logo 28px alineado izquierda + nombre org. Sin hero image.
- Cuerpo: H1 18px sans 600, párrafo 14px line-height 1.6 color `#1B2B4B`.
- Tabla factura: bordes finos, alineación derecha en importes, total weight 600 sobre `#f5f7fb`.
- CTA único: botón rectangular `#3D7BF5` blanco, 12px 24px padding, radius 6px.
- Footer 12px gris `#7a8499` con dirección fiscal del emisor + unsubscribe.

**Evitar a toda costa**:
- Gradientes morado/rosa.
- Glassmorphism con blur en cards (atrapa fixed children por stacking context).
- Emojis Unicode.
- Ilustraciones isométricas / Spline / Lottie.
- Tablas sin sticky header con 50 columnas.
- Modales con 3 niveles de scroll.
- Toasts genéricos "✨ Listo!" / "🎉 Genial!".
- Web fonts custom (Filson NO carga fiable en clientes email — usar `system-ui, -apple-system, "Segoe UI", sans-serif` en emails. Filson SÍ en panel admin/cliente).

**Tone of voice copy** (datos antes que adjetivos):
- Subject: `Factura A-2025-0034 de Acme · 1.234,56 €`
- Recordatorio: `Te recordamos que la factura A-2025-0034 vence el 15 de mayo.`
- Cobrada: `Hemos recibido el pago de la factura A-2025-0034. Gracias.`
- Bounce: `No pudimos entregar este email. La dirección rebotó.`
- Empty state: `Aún no hay envíos.`

**Whitelabel**:
- **Free**: header con logo FacturaIA + nombre org pequeño debajo. Footer `Enviado con FacturaIA · facturaia.com` linkado.
- **Pro Standard**: header solo logo de la org + nombre. Footer con dirección fiscal de la org + línea 10px gris `Powered by FacturaIA`.
- **Pro Plus**: sin marca FacturaIA en absoluto. Diferenciador comercial real.
- From: `facturas@dominio-cliente.com` con DKIM/SPF firmados.

---

## 2. Plan de implementación — 5 PRs secuenciales

### PR 1 — Mailer core + auth emails via Resend

Migration `059_email_core.sql`:
- `email_log` (PARTITION BY RANGE sent_at, RLS service_role).
- `email_suppressions` (UNIQUE email+scope, RLS service_role).
- `webhook_events_seen` (provider, event_id PK).

Código:
- `src/lib/mailer/provider/resend.ts` (cliente Resend + circuit breaker básico).
- `src/lib/mailer/log.ts` (escribir email_log).
- `src/lib/mailer/suppressions.ts`.
- Reemplazar `nodemailer` en `src/lib/email/send-factura.ts` y `send-presupoupuesto.ts` (mantener firma de la función pública para no tocar callers).
- 1 plantilla mínima: `factura-emitida.tsx` (React Email, estilo Stripe).
- Webhook `/api/webhooks/resend/route.ts` con HMAC verify + dedupe por PK + ingest a `email_log` + auto-suppress en hard bounce/complaint.
- Configurar Supabase Auth → Custom SMTP Resend con dominio `auth.facturaia.agentesia.world`.

Tests Vitest:
- HMAC verify (válido, inválido, replay).
- Suppression (insert idempotente, lookup pre-send).
- Adapter Resend mockeado.
- Auto-suppress en hard bounce.

### PR 2 — Outbox unificado + cola + plantillas core

Migration `060_email_outbox.sql`:
- ALTER `outbox_events` ADD COLUMN `kind text NOT NULL DEFAULT 'webhook'` + check `kind IN ('webhook','email')`.
- ADD COLUMN `idempotency_key text` UNIQUE PARTIAL `WHERE kind='email'`.
- Helper SQL `pg_partman` setup para `email_log` (N+2 meses adelante).

Código:
- `src/lib/mailer/queue/enqueue.ts` (con idempotency caller→enqueue).
- `src/lib/mailer/queue/dispatcher.ts` (`SELECT FOR UPDATE SKIP LOCKED` + Resend Batch 100/req).
- Endpoint `/api/internal/email-dispatcher` con `x-service-key` (cron 1 min).
- Throttle per-org: trigger BEFORE INSERT en outbox que cuenta últimos 60min y aborta >1000.
- List-Unsubscribe RFC 8058 con HMAC token (header + endpoint `/unsubscribe`).
- 7 plantillas más React Email: `presupuesto-emitido`, `proforma-emitida`, `abono-emitido`, `recordatorio-pre-vencimiento`, `factura-vencida`, `recordatorio-d15`, `bienvenida-org`.
- Cron Dokploy: añadir job para `/api/internal/email-dispatcher` cada 1 min con `curl -sf -X POST $URL -H "x-service-key: $FACTURAIA_SERVICE_KEY"`.

Tests:
- Idempotency: doble enqueue mismo key → 1 envío.
- Race: 2 workers concurrentes, ningún email duplicado.
- Throttle: org bombardea, queue lo corta.
- List-Unsubscribe: token válido borra de lista, inválido 403.

### PR 3 — Notifications multi-canal

Migration `061_notifications_channels.sql`:
- ALTER `notifications` ADD COLUMN `channels jsonb DEFAULT '["inapp"]'::jsonb`.
- ADD COLUMN `delivery_status jsonb DEFAULT '{}'::jsonb`.
- Nueva tabla `notification_deliveries (id, notification_id, channel, status, provider_id, error, sent_at)` con RLS service_role.
- Nueva tabla `notification_preferences (user_id, org_id, kind, channels[], digest, quiet_hours, PK compuesta)` con RLS por user_id.
- Backfill: notifications existentes con `channels=['inapp']`.

Código:
- Adaptar `useNotifications` para mostrar badge de canal por notif (icono pequeño 12px sobre/whatsapp/campana).
- Drawer notifs con tabs internos `Todas | In-app | Email | WhatsApp`.
- Trigger `trg_facturas_resolve_notifs` adaptado: cuando se resuelve, NO borrar; marcar `dismissed_at` y dejar histórico.
- Helper `enqueueNotification({orgId, userId, kind, channels, payload})` que escribe `notifications` + `outbox_events` (kind=email) en misma transacción.
- API `/api/notifications/preferences` GET/PATCH con `withApiAuth`.

Tests:
- Notif con channels=`['inapp','email']` crea 1 row notifications + 1 outbox.
- Notif con preferences que silencia email → solo inapp.
- Quiet hours respetadas.

### PR 4 — Módulo "Comunicaciones" + UI cliente

Migration `062_email_module.sql`:
- INSERT en `module_metadata` con `feature_id='comunicaciones'`, tagline, descripción larga, acciones, ia_prompt, `config_schema` para preferencias.
- INSERT en `features` (id='comunicaciones', category='modulo_ia').
- Asignar a planes Starter/Pro/Enterprise en `plan_features`.

Código:
- Tarjeta en `/agentes` linkando a `/settings/comunicaciones` (página completa, no modal).
- `/settings/comunicaciones/page.tsx` con 3 tabs (Preferencias · Plantillas · Dominio + historial).
- Componentes nuevos:
  - `EmailPreviewFrame` — iframe srcdoc para render email.
  - `DnsRecordCard` — card con tipo/host/valor + copy button + estado en vivo.
  - `VariableChipsPalette` — chips clicables agrupados (Cliente/Factura/Org), insert en cursor.
  - `EmailHistoryTable` — 5 columnas + expand-row + filtros visibles.
  - `TemplateEditor` — split-pane 40/60.
- Reutilizar `EstadoPill` extendiendo MAP con familia email (sent/delivered/opened/bounced/complained/failed) — colores que NO chocan con factura cobrada/pendiente/vencida.
- Iconos nuevos en `src/components/layout/icon.tsx`: `mail`, `mail-open`, `mail-bounced`, `globe-check` (SVG line-art `stroke="currentColor" strokeWidth={1.6} fill="none"`).

Tests E2E Playwright:
- Cliente activa preferencia email para factura_emitida → emite factura → email enviado.
- Cliente desactiva digest → no recibe agrupado.
- Override de slot por org se respeta en envío.

### PR 5 — Admin UI + custom domain + IA

Migration `063_email_templates_domains.sql`:
- `email_templates (template_key PK, current_version, category, is_blockable, default_channels, variables_schema)`.
- `email_template_versions (id, template_key FK, version_num, content jsonb, ai_generated, ai_prompt, changelog, published_by, published_at, canary_pct, metrics)`.
- `email_template_admin_overrides (template_key PK, forced_slots, default_slots, legal_footer, updated_by, updated_at)`.
- `email_template_org_overrides (org_id, template_key, slots, enabled, updated_by, updated_at, PK compuesta)` con RLS por org.
- `org_email_domains (id, org_id, domain, from_address, from_name, resend_domain_id, status, dns_records, dns_check_results, last_check_at, verified_at, is_default, txt_challenge, disabled_reason)` con RLS service_role para `dns_records`/`txt_challenge`.

Código:
- `/admin/comunicaciones/page.tsx` con 3 tabs (Plantillas · Operaciones · Salud).
- Editor plantillas con preview en vivo + canary publish (1% orgs 24h antes de full rollout).
- Endpoints `/api/admin/comunicaciones/*` con `withApiAuth({require:'superadmin'})`.
- Endpoint `/api/settings/email-domains` que crea TXT challenge único, llama Resend API, devuelve registros DNS.
- Cron `/api/internal/domain-verifier` cada 15min: re-verifica TXT, DKIM, SPF.
- 3 features IA reusando `ai_module_suggestions`:
  - Recordatorio cobros con tono adaptativo (lee `cobros` config existente).
  - Anomaly detector de gasto (señal módulo `antifraud`).
  - Smart send time (P95 open rate por org).
- Anti prompt-injection: XML wrapping `<user_template>...</user_template>` en system prompt + tool calls deshabilitadas en agentes que leen contenido externo.
- Cron diario único nocturno consolidado para los 3 IA.

Tests:
- Custom domain: TXT challenge único per-org, blocklist TLDs, re-verify drift.
- Canary: 1% orgs reciben versión nueva, resto la vieja.
- IA insights con prompt injection en plantilla → wrapping bloquea ejecución.
- Rollback plantilla a versión N en 1 click.

---

## 3. Setup Resend (a hacer manualmente antes de PR 1)

### En Resend Dashboard

1. Crear cuenta con `m.delmonte.p@agentesia.madrid`. Region: **EU (Ireland)**.
2. API Keys → Create → nombre `facturaia-prod`, scope "Full access" → copiar `re_...`. **Una sola API key sirve para ambos dominios**.
3. Domains → Add Domain DOS veces:
   - `mail.facturaia.agentesia.world` (transaccional negocio).
   - `auth.facturaia.agentesia.world` (Supabase Auth).
4. En cada dominio marcar **"Use a subdomain for return-path"**. Cada uno da 5 records DNS distintos.
5. Webhooks → Add → URL `https://facturaia.agentesia.world/api/webhooks/resend`. Eventos: todos (sent, delivered, bounced, complained, opened, clicked, delivery_delayed, scheduled, failed). Copiar signing secret `whsec_...`.

### En Cloudflare DNS

Pegar los 10 records totales (5 por dominio): SPF TXT, DKIM CNAME, MX bounces, DMARC TXT, Return-Path TXT.

**Proxy = OFF (gris) en TODOS**. Si naranja, MX y DKIM rompen.

Esperar 10-30 min. Click Verify en Resend para cada dominio hasta verde.

### En Supabase Dashboard

- Project → Authentication → SMTP Settings:
  - Enable Custom SMTP: **ON**
  - Sender email: `auth@auth.facturaia.agentesia.world`
  - Sender name: `FacturaIA`
  - Host: `smtp.resend.com`
  - Port: `465`
  - Username: `resend`
  - Password: API key `re_...`
- Project → Authentication → URL Configuration:
  - Site URL: `https://facturaia.agentesia.world` (sin barra final).
  - Redirect URLs: añadir `/login`, `/nueva-contrasena`, `/verificar-email`.
- Project → Authentication → Email Templates: revisar textos en español o personalizar.

### En Dokploy env vars

```
RESEND_API_KEY=re_xxx
RESEND_WEBHOOK_SECRET=whsec_xxx
EMAIL_FROM_ADDRESS=facturas@mail.facturaia.agentesia.world
EMAIL_FROM_NAME=FacturaIA
EMAIL_REPLY_TO_DEFAULT=hola@agentesia.world
EMAIL_AUTH_FROM_ADDRESS=auth@auth.facturaia.agentesia.world
EMAIL_WORKER_BATCH_SIZE=100
EMAIL_WORKER_MAX_RETRIES=6
```

Apply + Redeploy.

---

## 4. Plantillas iniciales (8 core, fase 1)

| # | template_key | Disparo | PR |
|---|---|---|---|
| 1 | `factura_emitida` | Al emitir factura desde UI o voz, cliente final recibe PDF | 1 |
| 2 | `presupuesto_emitido` | Idem para presupuesto | 2 |
| 3 | `proforma_emitida` | Idem para proforma | 2 |
| 4 | `abono_emitido` | Tras anular factura → abono al cliente | 2 |
| 5 | `recordatorio_pre_vencimiento` | -3 días del due_date, factura aún pendiente | 2 |
| 6 | `factura_vencida` | due_date pasó, sin cobro | 2 |
| 7 | `recordatorio_d15` | 15 días tras vencimiento | 2 |
| 8 | `bienvenida_org` | Org nueva creada, primer email al propietario | 2 |

**Auth (gestionados por Supabase, no por nuestra cola)**:
- `confirmation` (signup verify).
- `recovery` (password reset).
- `magic_link`.
- `email_change`.
- `invite`.

Resto bajo demanda fase 2+.

---

## 5. Variables de entorno totales

```
# Resend
RESEND_API_KEY=re_xxx
RESEND_WEBHOOK_SECRET=whsec_xxx
EMAIL_FROM_ADDRESS=facturas@mail.facturaia.agentesia.world
EMAIL_FROM_NAME=FacturaIA
EMAIL_REPLY_TO_DEFAULT=hola@agentesia.world
EMAIL_AUTH_FROM_ADDRESS=auth@auth.facturaia.agentesia.world
EMAIL_WORKER_BATCH_SIZE=100
EMAIL_WORKER_MAX_RETRIES=6

# Service key (cron interno) — ya existe
FACTURAIA_SERVICE_KEY=...

# Webhook signing — ya existe
WEBHOOK_SIGNING_KEY=...

# Anthropic — ya existe
ANTHROPIC_API_KEY=...
```

---

## 6. Métricas de éxito

| Métrica | Target |
|---|---|
| Email delivery rate | >98% |
| Email bounce rate | <2% |
| Email complaint rate | <0.1% |
| Custom domains verificados (orgs Pro) | >30% mes 1 |
| P99 enqueue → sent | <30s |
| P95 webhook ingest | <2s |
| Webhook events perdidos | 0 |
| Insights IA aplicados/desestimados | >70% |

---

## 7. Huecos de escalabilidad preparados

| Necesidad futura | Hueco | Coste activación |
|---|---|---|
| Multi-currency | currency en `email_log` | 1-2 días |
| Multi-language plantillas | `email_template_versions.locale` | 3-5 días/idioma |
| BIMI / ARC headers | Headers wrapper en provider/resend.ts | 2 días |
| Failover SES | Provider router | 2 días |
| WhatsApp canal real | Subscriber pattern en `notification_deliveries` | 1 semana (workflow voz ya existe) |
| Slack/Teams webhook | Mismo patrón | 3 días |
| A/B testing plantillas | `email_template_versions.canary_pct` ya en migration | 1 semana |
| List management (newsletter) | Tabla `email_lists` + endpoint subscribe | 2-3 días |

---

## 8. Reglas de proyecto aplicadas

De `CLAUDE.md` (proyecto + global):

- ✅ Toda tabla nueva con RLS en misma migración.
- ✅ `withApiAuth` / `withApiV1` patterns canónicos.
- ✅ Zod sintaxis v3 (`z.string().email()`, etc.) aunque v4 instalado.
- ✅ Single source of truth: extensión de `notifications` existente, NO paralela.
- ✅ Reuso de `outbox_events` existente para email + webhook.
- ✅ Reuso de `ai_module_suggestions` para insights, NO tabla nueva.
- ✅ Cambios quirúrgicos (no tocar lógica existente fuera del scope).
- ✅ Idempotency en endpoints públicos.
- ✅ Anti-pattern detectado: enum legal hardcodeado → motivos R1-R5 en plantilla `abono_emitido` con select.
- ✅ Skeleton solo si `items.length === 0`, sino stale-while-revalidate.
- ✅ `<Icon>` componente, NO emojis Unicode.
- ✅ `EstadoPill` MAP extendido (no sobrescrito) para no chocar con familia factura.

---

## 9. Lo que NO incluye este plan

- Stripe billing (proyecto separado, fase posterior).
- Listmonk / newsletter / marketing emails (cuando haya >500 leads).
- Stripe Tax automático.
- Multi-region failover.
- Push notifications móvil (iOS/Android).
- Affiliate tracking.
- Cripto / pagos alternativos.

---

## 10. Manuales a actualizar (al cierre de la implementación)

- `docs/manuals/manual-usuario.md` sección **"Comunicaciones"**: preferencias por evento × canal, plantillas (override slots si plan lo permite), historial, dominio propio.
- `docs/manuals/manual-admin.md` sección **"Comunicaciones"**: gestión global plantillas, per-org override, métricas, modo mantenimiento, custom domain admin, IA insights.

---

## 11. Próximos pasos inmediatos

1. **Manuel**: setup Resend manual (cuenta + 2 dominios + DNS Cloudflare + Supabase SMTP + Dokploy env vars). ~1h.
2. Cuando termine, decir "listo Resend".
3. **Claude**: arrancar PR 1 (migration 059 + adapter Resend + reemplazo nodemailer + 1 plantilla + webhook + tests).
4. Review de PR 1 por Manuel antes de mergear.
5. Repetir para PR 2-5.

Tiempo estimado total: ~3 semanas calendario, ~1 PR por sesión activa.

---

## Referencias

- [[facturaia]] — hub maestro
- [[facturaia-integracion-api-v1-portal]] — patrón outbox que se reutiliza
- [Stripe email design](https://stripe.com/emails) — referente estética (no link interno, fuente externa)
- [Resend docs](https://resend.com/docs) — API + webhooks
- [List-Unsubscribe RFC 8058](https://datatracker.ietf.org/doc/html/rfc8058) — obligatorio Gmail/Yahoo 2024
- [React Email](https://react.email) — librería plantillas
- [pg_partman](https://github.com/pgpartman/pg_partman) — particionado mensual
- Repo: `AgentesIA-MAdrid/facturaia` — branch base `main`
