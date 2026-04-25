---
title: hot cache
date: 2026-04-17
tags: [stack, index]
---

# Hot Cache — Últimas 2 semanas

Patrones y soluciones recientes que probablemente se reutilicen pronto.
Se lee PRIMERO antes de buscar en el resto del vault.

> Si algo tiene más de 2 semanas aquí, moverlo al índice correspondiente en Stack/ o eliminarlo.

---

## Google Favicon API + auto-logo con sentinel not_found (2026-04-25)

Patrón para auto-asignar logos a proveedores/clientes sin intervención:

1. **API**: `https://www.google.com/s2/favicons?domain={slug}.es&sz=128` — gratis, sin key
2. **Slug**: nombre de empresa → quitar S.L./S.A., normalizar acentos, solo alfanumérico
3. **Filtro**: `byteLength > 750` descarta el globe default (~726 bytes)
4. **Modo strict** (auto): solo `{slug}.es` y `{slug}.com` — coincidencia exacta con nombre
5. **Modo broad** (manual): variantes (1ra palabra, 2 palabras, completo) × 5 TLDs
6. **Sentinel**: `logo_url = null` → buscar; `'not_found'` → ya buscado, no repetir; `'https://...'` → mostrar
7. **Best**: el favicon más grande en bytes = más detallado

Clearbit (`logo.clearbit.com`) ya no funciona — adquirida por HubSpot, API cerrada.

Ver [[clearbit-logo-api-ya-no-existe]] y [[google-favicon-api-patron-auto-logo]]

---

## FacturaIA — Impersonation con proxy client (2026-04-22)

Patrón para que superadmin vea datos de cualquier org sin tocar RLS:

1. **Middleware** lee `?impersonate=org_id`, valida superadmin, setea cookie `impersonate_org` (1h maxAge)
2. **Layout server** lee cookie → pasa `orgId` + `isImpersonating` al shell
3. **OrgContext** React context con `useOrg()` y `useOrgClient()` hooks
4. **Proxy client** (`createImpersonateClient(orgId)`) mimics Supabase fluent API pero rutea via `/api/admin/impersonate/query` POST
5. **Query proxy** server-side usa `createAdminClient()` (service_role, bypasses RLS), auto-añade filtro `org_id`
6. **Write stubs** — insert/update/delete/upsert devuelven error (read-only)

Gotchas al migrar componentes:
- `useOrgClient()` es hook → solo a nivel de componente, nunca dentro de useEffect
- Componentes con `auth.getUser()` → `org_members` chain **fallan** con proxy (user=null). Simplificar a query directa a `organizations` (proxy filtra por org_id)
- Realtime hooks (`useBandejaRealtime`) necesitan el proxy para carga inicial pero channels reales solo en modo normal
- useEffect deps deben incluir `[isImpersonating, orgId]` para re-fetch al cambiar org
- Helpers de módulo (fuera de componente) no pueden usar hooks → mantener `createClient` importado aparte

---

## Supabase Cloud — RLS multi-tenant con SECURITY DEFINER (2026-04-19)

Patrón para SaaS multi-tenant:
1. `get_user_org_id()` SECURITY DEFINER STABLE — lee org_id de org_members via auth.uid()
2. Todas las policies: `USING (org_id = get_user_org_id())`
3. Onboarding: `create_org_for_user(org_nombre)` crea org + inserta en org_members
4. `next_invoice_number(serie)` para auto-numeración con bloqueo de fila

Ver [[rls-multi-tenant-supabase-con-security-definer]]

## AI Agent con reservas — 3 reglas anti-bug (2026-04-19)

Para cualquier AI Agent n8n que gestione reservas con Google Calendar:

1. **0 eventos = todo libre** — añadir regla explícita en prompt, Think tool y tabla de herramientas. Los LLMs interpretan lista vacía como "no disponible"
2. **Weekday number en Think** — incluir `{{ $now.weekday }}` (1-7) + fórmula + ejemplos + verificación. Sin esto el LLM calcula mal "lunes" desde "sábado"
3. **Tool description con consecuencias** — para write-tools (Reservar, Cancelar), expandir descripción a ~280 chars explicando "sin esta llamada la acción NO ocurre". Descripción genérica = LLM genera texto sin ejecutar

Ver [[google-calendar-tool-0-eventos-significa-todo-libre]], [[llm-calcula-mal-dia-semana-a-fecha-sin-weekday-number]], [[tool-description-generica-no-fuerza-ejecucion-de-tool-critica]]

---

## Kommo webhook status_lead — siempre filtrar (2026-04-20)

`status_lead` dispara en TODOS los cambios de estado, no solo el target. Añadir IF `status_id == X` después del webhook para evitar ejecuciones duplicadas. Sin esto: emails duplicados, eventos Calendar duplicados, tareas duplicadas.

Ver [[kommo-webhook-status-lead-dispara-en-todos-los-cambios]]

## toolWorkflow onError — usar continueErrorOutput (2026-04-20)

En nodos toolWorkflow del AI Agent, `stopWorkflow` mata al agente sin respuesta al usuario. Usar siempre `continueErrorOutput`.

Ver [[toolWorkflow-onError-stopWorkflow-mata-al-agente-silenciosamente]]

---

## n8n API — importar workflows con control chars (2026-04-25)

Los JSON de workflows con nodos Code contienen `\n`/`\t` en `jsCode` que rompen shell escaping. Patrón seguro:

1. Python `json.dump(payload, f, ensure_ascii=True)` a `/tmp/`
2. `curl -d @/tmp/file.json` (nunca inline)
3. Parsear respuestas con `json.loads(raw, strict=False)` o grep
4. `executeWorkflowTrigger` v1.1 requiere input schema — usar v1.0 si no necesitas validación
5. Activar: `POST .../activate` (no PATCH/PUT). Actualizar: `PUT` (requiere `name`)

Ver [[n8n-api-importar-workflows-json-requiere-archivos-temporales]], [[n8n-executeWorkflowTrigger-v1.1-requiere-input-schema]], [[n8n-api-activate-es-POST-no-PATCH]]

## OCR pipeline facturas — patrón Next.js + n8n + OpenAI Vision (2026-04-20)

1. Next.js convierte archivo a base64 (`Buffer.from(arrayBuffer).toString('base64')`) — n8n Code Node sandbox no tiene `helpers.binaryToBuffer`
2. Enviar `org_nombre` en el webhook body para que el prompt distinga emisor vs receptor
3. Frontend simula progreso 0→90% con `setInterval` mientras `estado='procesando'`. Supabase Realtime sobrescribe con 100% al terminar
4. n8n actualiza `bandeja_ingesta` con PATCH directo a Supabase (no PostgREST)

Ver [[ocr-facturas-confunde-receptor-con-emisor-sin-org-nombre]], [[n8n-code-node-sandbox-no-tiene-helpers-binaryToBuffer]]

## Dokploy — Traefik reload obligatorio tras redeploy (2026-04-20)

Cada redeploy deja Bad Gateway. Contenedor arranca OK pero Traefik no re-descubre la ruta.
**Fix**: Dokploy → Settings → Web Server → Reload. Verificar contenedor con `ps aux` + `netstat -tlnp` antes.

Ver [[dokploy-requiere-reload-manual-traefik-tras-redeploy]]

## n8n $if isExecuted para ramas IF (2026-04-20)

En workflows con ramas condicionales, cualquier expresión que referencia un nodo de otra rama debe usar:

```
={{ $if($('Nodo').isExecuted, $('Nodo').item.json.campo, fallbackValue) }}
```

Sin esto: error silencioso que rompe la ejecución. Caso típico: contacto existente vs nuevo, cada uno crea por su rama pero un nodo posterior referencia solo una.

Ver [[n8n-expresion-nodo-no-ejecutado-falla-silencioso]]

## Calendar events formato limpio (2026-04-20)

Para Clínica Zen (y cualquier proyecto con Calendar):
- **Summary**: `Valoración - Odontología - Ana López` (legible en vista calendario)
- **Description**: Lead ID, teléfono, email, motivo, fuente (datos para gestión)

Google Calendar `query` busca en summary + description, así que poner Lead ID en description funciona para buscar/cancelar/mover eventos programáticamente.

---

## FacturaIA — Puppeteer HTML→PDF pixel-perfect (2026-04-25)

Patrón para PDFs idénticos al preview HTML: Puppeteer headless + `renderToStaticMarkup` + `page.setContent()`.

1. **Browser singleton** con idle timeout 60s — cold ~10s, warm ~2.3s
2. **Dynamic imports** obligatorios en Next.js 16 Route Handlers: `await import('react-dom/server')` (static import bloqueado)
3. **Quitar `'use client'`** de componentes de plantilla para poder llamarlos con `createElement()` desde server (funcionan igual client-side si el padre tiene la directiva)
4. **Fonts base64 inline** en `<style>` — per-template (2-3 fonts vs 10), cacheadas en `Map` a nivel módulo
5. **`page.setContent()`** vs `page.goto()` — elimina round-trip al dev server

API Route: `/api/render-pdf` (POST con `{ config, data }`). Excluir en `isServiceRoute` del middleware.

Ver [[puppeteer-html-to-pdf-pixel-perfect-con-plantillas-react]]

## FacturaIA — pdf-lib para generar PDFs server-side (2026-04-20)

PDFKit falla en Turbopack (ENOENT .afm). Usar pdf-lib: `PDFDocument.create()` + `StandardFonts`.
Seed: nunca insertar campos calculados (facturado, pendiente, gasto) — columnas no existen en BD.
API routes internas sin sesión: header `x-service-key` con service_role key.

Ver [[pdf-lib-funciona-en-nextjs-turbopack-donde-pdfkit-falla]], [[supabase-insert-silencioso-con-ts-nocheck-oculta-columnas-inexistentes]]

## FacturaIA — APIs admin devuelven objetos, no arrays (2026-04-21)

Las API routes admin devuelven objetos con campos nombrados, no arrays directos:
- `/api/admin/features` → `{ features, dependencies, orgCounts }`
- `/api/admin/plans` → `{ plans, orgCounts }`
- `/api/admin/plans/[id]/features` → `{ planFeatures, allFeatures }`
- `/api/admin/plans/[id]/limits` → array directo (excepcion)
- `/api/admin/orgs` → array directo
- `/api/admin/orgs/[id]/members` → array directo

Siempre desestructurar: `data.features || []`. Error causó crash en 3 páginas.

## FacturaIA — Admin Panel + Feature Flags arquitectura (2026-04-21)

Sistema completo de admin multi-tenant con feature flags:

**Tablas**: plans, features, feature_dependencies, plan_features, plan_limits, org_features, org_limits, admin_alert_dismissals + ALTER organizations (billing_status, trial_ends_at, onboarding, last_activity_at, plan FK) + ALTER profiles (is_superadmin)

**Feature resolution**: plan_features (defaults) → org_features (overrides). `org_has_feature(org_id, feature_id)` SQL function. Client-side: FeatureProvider carga via Supabase client, fail-open on error, polling 5min + visibility reload.

**Billing state machine**: trial → grace_period → expired → active/suspended/cancelled. Lazy expiration en server layout (no cron). `getOrgBilling()` evalúa trial_ends_at + grace_days en cada request.

**Admin auth**: doble barrera — middleware (redirect non-admin) + server layout (`isSuperadmin()`). Primero comprueba `SUPERADMIN_EMAILS` env, luego `profiles.is_superadmin`.

**Admin client**: `createAdminClient()` usa `SUPABASE_SERVICE_ROLE_KEY` (bypasses RLS). Todas las API routes admin usan `requireAdmin()`.

**13 API routes**: `/api/admin/stats`, `/api/admin/orgs` (GET/POST), `/api/admin/orgs/[id]` (GET/PATCH), `/api/admin/orgs/[id]/features|limits|billing|members`, `/api/admin/features` (GET/POST/PATCH), `/api/admin/plans`, `/api/admin/plans/[id]/features|limits`, `/api/admin/alerts`, `/api/admin/alerts/dismiss`

**Impersonation**: botón "Ver como esta org" en org detail → `/?impersonate=org_id`. Middleware valida que solo superadmin puede usar el param. ImpersonateBanner morado en dashboard.

## Conciliación bancaria IA — patrón prompt 2 fases (2026-04-21)

Pipeline para cruzar extractos bancarios con facturas:
1. Fase 1 (extracción): Claude parsea cualquier formato → JSON de movimientos
2. Fase 2 (matching): Claude recibe movimientos + facturas pendientes + reglas aprendidas → matches con score
- Prompt caching: facturas/reglas en bloque cached, solo movimientos dinámicos
- Scoring con tabla numérica fija (+50 importe, +25 nombre, +15 fecha, -100 descarte)
- Comparar siempre contra factura.total (con IVA), nunca base
- Hash dedup: cuenta+fecha+concepto+importe+idx (idx evita falsos positivos)
- Batches de 50 si >100 movimientos
- Umbral auto-aprobación: 95 para gestorías, configurable por org

Ver spec: `facturaia/docs/superpowers/specs/2026-04-21-conciliacion-bancaria-design.md`

---

## WhatsApp Cloud API — webhook per-phone-number override (2026-04-21)

Cuando la app Meta es compartida (ej: con Chatwoot), NO tocar el webhook a nivel app. Usar override por numero:

```bash
curl -X POST "https://graph.facebook.com/v22.0/{phone_number_id}" \
  -H "Authorization: Bearer $TOKEN" \
  -d 'webhook_configuration={"override_callback_uri":"https://...","verify_token":"..."}'
```

El webhook receptor (`zYcHHa8jWXB6dY5i`, nodo "Prepare Data") busca org comparando el número del **remitente** (`from`, normalizado sin prefijo 34) contra `settings.whatsapp.phone_number` de cada org. No usar `phone_number_id` (es el ID del número receptor, compartido entre todas las orgs).

## n8n binary data filesystem mode (2026-04-21)

En modo filesystem, `binaryData.data` devuelve `"filesystem-v2"` (referencia), no los bytes reales. Para obtener el contenido:

```js
const buffer = await this.helpers.getBinaryDataBuffer(0, 'data')
const base64 = buffer.toString('base64')
```

Nunca usar `$binary.data.data` directamente en expresiones — siempre Code Node con `getBinaryDataBuffer()`.

## Settings JSONB toggle sin race condition (2026-04-21)

Al hacer toggle sobre campos dentro de `settings` JSONB:
1. Guardar `settingsRef` en estado React al cargar
2. En toggle: derivar nuevo estado de `settingsRef` local, no releer de BD
3. Actualizar ambos: `setSettingsRef(new)` + `supabase.update({ settings: new })`

Releer de BD causa race condition: dos toggles rapidos, la segunda lectura sobreescribe la primera escritura.

## n8n workflow con 2 entry points — $if isExecuted para nodos compartidos (2026-04-21)

Cuando un workflow tiene webhook (Retell) + executeWorkflowTrigger (chatbot) y ambos convergen en un nodo downstream:

```
={{ $if($('Edit Fields Retell').isExecuted, $('Edit Fields Retell').item.json.campo, $('Edit Fields Chatbot').item.json.campo) }}
```

Sin esto: "Invalid expression" porque el nodo de la otra rama no se ejecutó. Caso real: `Create an event1` en Clínica Zen.

Ver [[n8n-nodos-compartidos-entre-ramas-requieren-if-isExecuted]]

---

## CLAUDE.md por proyecto — cascada de carga (2026-04-21)

Claude Code carga instrucciones en cascada según el directorio de trabajo:

1. `~/.claude/CLAUDE.md` → siempre (global, ~150 líneas max)
2. `<repo>/CLAUDE.md` → solo al trabajar en ese repo
3. `<repo>/src/CLAUDE.md` → herencia por subcarpeta (si existe)

Cada nivel suma, no reemplaza. Gotchas específicos van en el CLAUDE.md del repo (ej: `facturaia/CLAUDE.md` con 20 reglas de schema/frontend/auth). Conocimiento técnico profundo va en `Stack/` y se carga bajo demanda via la tabla de "lectura por tema" del global.

Ver [[claude-md-por-proyecto-reduce-tokens-y-carga-solo-lo-relevante]]

---

## Redis debounce — verificar nombres de campo entre ramas (2026-04-22)

Cuando un Merge recibe inputs de ramas distintas (texto=`Mensaje`, audio=`text`), el Redis SET debe contemplar TODOS los campos posibles:

```
$('Merge').first().json.Mensaje || $('Merge').first().json.text || ''
```

Sin el fallback, la rama que usa un campo diferente guarda vacío → el IF post-debounce descarta el mensaje silenciosamente. No hay error visible.

Ver [[redis-debounce-campo-nombre-diferente-pierde-mensajes]]

## Kommo salesbot — puede mover leads sin n8n (2026-04-22)

Los salesbots de Kommo tienen lógica interna (GUI) que puede incluir "Cambiar etapa". Cuando n8n dispara `POST /api/v2/salesbot/run`, el bot ejecuta TODA su cadena — incluyendo cambios de estado invisibles para n8n.

Síntoma: lead cambia status entre ejecuciones sin que ningún sub-workflow lo haga. Debug: revisar salesbot en GUI Kommo → buscar acciones "Cambiar etapa".

Ver [[kommo-salesbot-puede-mover-leads-de-estado-sin-n8n]]

---

## Compose n8n producción — checklist anti-caídas (2026-04-22)

Antes de desplegar n8n para cualquier cliente, verificar estos 4:

1. **Healthcheck HTTP** — `wget -qO- http://localhost:5678/healthz || exit 1` (interval 30s, retries 3, start_period 60s)
2. **Pruning** — `EXECUTIONS_DATA_PRUNE=true` + `MAX_AGE=168` + `MAX_COUNT=5000`
3. **Memory limit** — `deploy.resources.limits.memory: 2G` + `NODE_OPTIONS=--max-old-space-size=1536`
4. **Versión fija** — nunca `:latest`, usar tag exacto (ej: `n8nio/n8n:2.15.1`)

Sin healthcheck, n8n se cuelga sin crashear y Docker no lo reinicia. Sin pruning, las ejecuciones acumuladas son la causa del hang.

Compose de referencia: `~/n8n-agentesia-world-compose.yml`

Ver [[n8n-se-cuelga-sin-crashear-necesita-healthcheck-http]]

---

## Email OAuth Gmail + polling configurable por org (2026-04-24)

Patron completo para ingesta de facturas via email:

1. **OAuth connect**: Google OAuth2 con HMAC state validation, tokens en `settings.email.oauth_token/refresh_token` JSONB
2. **Polling endpoint** (`/api/email/poll`): service-key auth con `timingSafeEqual`, per-org interval check (`settings.email.poll_interval_minutes`), skip si `elapsed < intervalMs`
3. **Manual poll** (`/api/email/poll-now`): session-authenticated, procesa solo la org del usuario
4. **n8n schedule**: 30min como base minima, per-org intervals (1h/2h/6h/12h/24h) filtrados en el endpoint
5. **Dedup**: SHA256 hash de cada attachment, check contra `bandeja_ingesta.file_hash` antes de insertar
6. **OCR webhook**: fire-and-forget con timeout 30s y 3 retries al n8n OCR pipeline existente
7. **last_checked**: solo avanza al timestamp del ultimo email procesado con exito (no al final del batch)

Archivos clave: `src/lib/email/`, `src/app/api/email/poll/`, `src/app/api/auth/google/`, `n8n/workflows/email-polling.json`

---

## Supabase Storage — calcular uso real via SDK, no SQL (2026-04-25)

`storage.objects.metadata->>'size'` no es fiable — puede ser NULL aunque el archivo exista. La Storage API computa el tamaño al leer. Para calcular storage por org:

```ts
const { data: files } = await admin.storage.from('facturas').list(orgId, { limit: 1000 })
const storageMb = Math.ceil(files?.reduce((sum, f) => sum + (f.metadata?.size || 0), 0) / 1048576)
```

Nunca usar RPCs SQL para esto. Ver [[supabase-storage-objects-metadata-no-es-fiable-para-size]]

---

## FacturaIA — complimentary orgs para MRR (2026-04-25)

Campo `complimentary` boolean en `organizations` (default false, migración puso true a las existentes). Patrón:

- MRR SQL: `WHERE billing_status = 'active' AND NOT complimentary`
- `admin_dashboard_stats` devuelve `complimentary_orgs` y `paying_orgs` además de `mrr`
- Admin dashboard: banner de aviso cuando todas son complimentary, KPI MRR en amarillo
- Lista orgs: estrella morada a la izquierda del nombre (con tooltip)
- Detalle org > Billing: toggle complimentary con explicación

Cuando se integre Stripe: poner `complimentary = false` al activar método de pago.
Migración: `007_complimentary_orgs.sql`. Schema Zod: `adminUpdateOrgSchema` incluye `complimentary: z.boolean().optional()`.
