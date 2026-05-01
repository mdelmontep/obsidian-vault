---
title: FacturaIA ↔ agency-portal — Integración API v1 + Webhooks
date: 2026-05-01
source: claude-code-session
tags: [facturaia, agency-portal, api, webhooks, integracion, agentesia]
estado: review-pendiente
---

# Integración FacturaIA ↔ agency-portal

Sesiones 30-abril a 1-mayo-2026 con Claude Code. **PRs portal P1-P7 listos para review de Borja. Auditoría completa con fixes commiteados. PR-A3 facturaia (#32) pendiente de cerrar.**

## Update 2026-05-01 — Auditoría y fixes (Stripe-style sync pattern)

Tras ejecutar 7 PRs apilados en agency-portal, auditoría completa identificó y corrigió 7 bugs sustantivos (commits dentro de cada PR para que Borja vea continuidad limpia):

- **HMAC receiver**: distinguir transient (5xx/red) vs permanent (4xx) → DELETE log en transient. Ver [[webhook-idempotency-borrar-log-en-errores-transitorios]]
- **Sombra duplicada**: UPSERT por `remote_id` (no por `id` local) en `auto-emit` y `emit-from-stripe`. Ver [[upsert-sombra-por-id-remoto-no-por-id-local]]
- **Path traversal**: validar `path.charAt(36) === '/'` después del UUID en `/api/documents/file`. Ver [[checklist-seguridad-api-routes-nextjs]] item 11
- **PostgREST cache**: `NOTIFY pgrst, 'reload schema';` al final de migration. Ver [[postgrest-schema-cache-notify-tras-migration]]
- **Signed URL TTL**: endpoint proxy `/api/facturaia/pdf/[shadowId]` regenera on-demand. Ver [[signed-url-proxy-endpoint-vs-cached-en-bd]]
- **PostgREST `.or()` injection**: sanitizar `%_,():.\\*"` antes de search.
- **TS narrowing openapi-fetch ternary**: split if-else literal. Ver [[openapi-fetch-ternary-rompe-narrowing-typescript]]

Arquitectura final: **Stripe-style bidirectional sync** = (1) webhook tiempo real, (2) cron reconciliación, (3) backfill manual. Tres capas para tolerancia a fallos.

Slack draft creado en `#pro-portal-clientes` (channel_id `C0AV7NAEJDA`, draft_id `Dr0B110KG30S`) — pendiente de enviar manualmente por Manu.

## Por qué se hace

El portal `agency-portal` (Next.js, multi-tenant para Agentesia) necesita emitir documentos fiscales legales. Tiene su propio sistema comercial (`quotes`, `agency_invoices`, `contracts`) pero no es source of truth fiscal — no tiene Verifactu, ni numeración correlativa AEAT, ni motivo R1-R5.

**Modelo decidido (A — replicación)**:
- Lo comercial vive en el portal (quote → contract → agency_invoice)
- Lo fiscal se replica en FacturaIA vía API REST cuando se "emite oficialmente"
- FacturaIA es source of truth de numeración + Verifactu + PDF oficial
- El portal guarda `facturaia_documents.remote_id` y muestra el PDF de FacturaIA

Razón: el cliente final solo ve UN documento (el de FacturaIA), cero duplicación de números fiscales, AEAT solo conoce un emisor.

## Plan de PRs (7 total)

### FacturaIA (lado servidor — 3 PRs)

| PR | Estado | URL | Qué hace |
|---|---|---|---|
| PR-A1 | ✅ MERGED | #29 | Foundation: `api_keys` (sha256+prefix+scopes+mode), `api_idempotency`, `api_request_log`, `motivo_rectificacion` R1-R5, `organizations.is_test`, partial UNIQUE clientes(org_id,nif,pais), lib `src/lib/api/` (auth, errors, response, idempotency, rate-limit, handler), UI Settings → API Keys. Migration 023 |
| PR-A2 | ✅ MERGED | #30 | Endpoints `POST/GET /v1/facturas`, `POST/GET /v1/presupuestos`, `GET /v1/health`, `GET /v1/openapi.json`. Service compartido `src/lib/documents/create-document.ts` |
| PR-A2.5 | ✅ MERGED | #31 | Listings cursor-paginated, `POST /v1/facturas/[id]/anular`, `POST /v1/presupuestos/[id]/cancelar`, `GET /v1/{tipo}/[id]/pdf` (signed URL). Bug fixes: `facturas.fuente` permite 'api', `presupuestos.estado` permite 'cancelado', upsert cliente respeta `pais IS NULL`. Migration 024 |
| **PR-A3** | 🟡 ABIERTO #32 | https://github.com/AgentesIA-MAdrid/facturaia/pull/32 | Webhooks salientes HMAC + outbox + dispatcher. Migration 025. **PARCIALMENTE VALIDADO** (ver abajo) |

### agency-portal (lado cliente — 4 PRs, todos pendientes)

- PR-P1 — SDK autogenerado de OpenAPI (`openapi-typescript`) + cliente HTTP `openapi-fetch` + tabla `facturaia_documents` (id, type, remote_id, num, pdf_url, estado, sync_at, agency_invoice_id?, quote_id?, billing_invoice_id?) + receiver `/api/webhooks/facturaia` con HMAC verify + env vars `FACTURAIA_*`
- PR-P2 — Server actions `emitAgencyInvoiceFiscally`, `emitQuoteFiscally`. Botón "Emitir oficialmente" en UI. PDF interno pasa a borrador, oficial es el de FacturaIA
- PR-P3 — Stripe webhook `invoice.paid` → `POST /v1/facturas` automático. Idempotency-Key derivada de `stripe_invoice_id`
- PR-P4 — Hardening: monitoreo de `webhook_deliveries`, rotación API key documentada, E2E manual

## Estado actual de PR-A3 (lo que dejamos a medias)

**Branch**: `feat/api-v1-webhooks` (PR draft #32 abierto, base `main`).

### Qué funciona end-to-end (validado en local 30-abril)
- ✅ POST `/api/v1/facturas` real con curl → 201 + factura `A2026-0006` creada con PDF y Verifactu encolado
- ✅ Trigger BD insertó evento en `outbox_events` + delivery en `webhook_deliveries`
- ✅ Dispatcher (`POST /api/internal/webhook-dispatcher` con `x-service-key`) firmó HMAC y entregó
- ✅ webhook.site recibió POST con headers `X-FacturaIA-Event-Id`, `X-FacturaIA-Event-Type: factura.created`, `X-FacturaIA-Signature: t=<unix>,v1=<hmac>`, `X-FacturaIA-Delivery-Attempt`, body envelope `{id, type, created_at, org_id, data}`
- ✅ Validador SSRF: 11 casos pasados directamente (privadas, loopback, IPv6, .local, .internal, localhost rechazados; webhook.site y dominios reales aceptados)

### Bugs detectados durante validación (todos arreglados en branch, pendientes de commit)
1. **Middleware `src/proxy.ts` → `updateSession()` interceptaba `/api/v1/*` y `/api/internal/*`** redirigiendo a `/login`. Hacía toda la API pública inutilizable para consumers externos. Fix: añadidas a `isServiceRoute` en `src/lib/supabase/middleware.ts:75-86`
2. **`X-FacturaIA-Delivery-Attempt` off-by-one**: enviaba "attempt=2" en el primer intento. Fix: `String(attempt)` en lugar de `String(attempt + 1)` en `src/lib/webhooks/dispatcher.ts`

### Qué NO se validó manualmente (no son blockers)
- Reintentos con backoff exponencial cuando recv da 5xx (httpstat.us/500)
- Evento `factura.anulada` (sale gratis cuando el portal anule cualquier factura)
- Auto-pausa tras 50 fallos consecutivos
- Verificación de firma manualmente con node script

### Próximo paso elegido (camino A)
Antes de mergear PR-A3, **escribir un script de Node que pruebe reintentos sin depender del dev server**. El script:
1. Conecta a Supabase remoto con service_role
2. Inserta un delivery falso apuntando a `httpstat.us/500`
3. Llama a `dispatchPending()` directamente
4. Verifica que la fila quedó `status='retry'`, `attempt=2`, `retry_at` futuro

Output esperado: `✅ retry registrado correctamente`. Si pasa → commit + merge PR-A3.

### Por qué no se completó: dev server local con problemas (Turbopack EPIPE/ECONNRESET, tarda 3+ min en compilar). No bloquea el script automatizado.

## Configuración necesaria para producción (cuando se mergee PR-A3)

**Env vars en Dokploy (FacturaIA)**:
```
WEBHOOK_SIGNING_KEY=<32+ chars hex>      # AES-256-GCM para cifrar secrets
FACTURAIA_SERVICE_KEY=<existing>          # Reusable del que ya hay
```

**Cron Dokploy cada 1 min** (no hay 30s nativo):
```
*/1 * * * * curl -s -X POST -m 25 -H "x-service-key: $FACTURAIA_SERVICE_KEY" https://facturaia.com/api/internal/webhook-dispatcher >/dev/null
```

**Migraciones aplicadas en remoto (verificadas)**:
- 023_api_v1_foundation
- 024_api_v1_extensions
- 025_webhooks

## Decisiones de arquitectura tomadas

- **Single-tenant en la práctica**: org Agentesia (`ea201784-4813-4eae-ac3f-9cffdb9cc24a`) único consumer del portal. Una sola API key live emitida (`fia_live_...` guardada en `agency-portal/.env.local` como `FACTURAIA_API_KEY`)
- **Mode test/live**: `organizations.is_test=false` por defecto. Para sandbox del portal habría que crear "Agentesia (Test)" como org separada con `is_test=true`. Pendiente decisión
- **Cliente upsert por NIF**: clave compuesta `(org_id, lower(nif), coalesce(pais,'España'))` con partial UNIQUE. La función `resolveCliente` matchea legacy NULL pais cuando se pide 'España'
- **Idempotency Stripe-style**: header obligatorio en POST, body hash sha256, 24h cache, mismo key + body distinto → 422 conflict
- **Webhooks transaccionales**: triggers BD insertan en outbox dentro de la misma tx que la mutación. Cero fantom events
- **Cifrado de secrets webhook**: AES-256-GCM con `WEBHOOK_SIGNING_KEY` (fallback `CREDENTIAL_ENCRYPTION_KEY`). El dispatcher descifra antes de firmar; secret plano se devuelve UNA vez al crear

## Pendiente conceptual (no PR concreto todavía)

- **Bug UI: factura "generada" en UI no llegó a BD** — durante validación creamos A2026-0004 desde UI dashboard, devolvió OK pero no se insertó. Última factura real en BD: `E-2026-040`. Probable error en endpoint de creación manual sin log visible. Investigar en sesión futura
- **DNS rebinding** en webhook URLs: out of scope PR-A3. Solución sería resolver hostname antes de fetch y comparar IP. Sin esto, un atacante podría registrar un webhook a un dominio que rota su DNS entre IP pública e IP privada
- **Bucket `facturas` es público** en Storage. Las URL de POST `/v1/facturas.pdf_url` son inmortales. PR posterior debería migrar el bucket a privado y forzar uso de `GET /v1/{tipo}/[id]/pdf` (firmado TTL 5min)

## Stack del agency-portal (para PR-P1)

```
Next.js 16.2.1, React 19.2.3, TypeScript strict
Supabase SSR, Tailwind 4 + shadcn (base-nova)
Zod v4 (ojo: FacturaIA usa Zod v3 forzado)
@react-pdf/renderer, Stripe v22, OpenAI, Retell SDK
```

Dominios existentes (importante para no duplicar):
- `prospects` → `quotes` → `contracts` → `agency_invoices`
- `billing_profiles` + `invoices` (Stripe subscriptions del cliente)
- Memberships agency_admin/manager/developer/client_owner/member/read_only

Hierarchy: **Agency → Client → Project**. Cookie `agency_portal_active_tenant` resuelve tenant activo.

## Cómo retomar en próxima sesión

Frase para arrancar (después de reiniciar Mac):

> "Retomamos integración FacturaIA ↔ agency-portal. Lee /Users/manueldelmonte/Obsidian/Manu/knowledge/projects/agentesia/facturaia-integracion-api-v1-portal.md para contexto. Estábamos en PR-A3 webhooks, parcialmente validado, pendiente de un script Node que pruebe reintentos sin depender del dev server local. Después de eso commit + merge PR-A3, luego empezamos PR-P1 en agency-portal."
