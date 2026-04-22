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

## Retell → n8n checklist (2026-04-18)

Antes de subir un prompt de Retell que conecta con webhooks de n8n:

1. URLs de tools apuntan al dominio correcto (`dig +short` para verificar — EasyPanel ≠ dominio custom)
2. Cada tool referenciada en el prompt existe en `general_tools`
3. Nombres de parámetros coinciden con `Edit Fields` / `Set` del workflow n8n
4. Workflow destino activo y no archivado
5. `parameter_type: "json"` si n8n espera `body.args.X`

Ver [[retell-parameter-type-form-vs-json-rompe-n8n-silenciosamente]] y [[easypanel-y-dominio-custom-pueden-resolver-a-ips-distintas]]

## Slack API — escribir en canvas (2026-04-18)

```bash
# 1. Unir bot al canal
curl -s -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"channel":"C0ARS4X5MF0"}' "https://slack.com/api/conversations.join"

# 2. Editar canvas (insert al final)
curl -s -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json; charset=utf-8" \
  -d '{"canvas_id":"F0AT6KEJLQZ","changes":[{"operation":"insert_at_end","document_content":{"type":"markdown","markdown":"- [ ] Tarea nueva\n"}}]}' \
  "https://slack.com/api/canvases.edit"
```

- Canvas Tareas Pendientes: file_id `F0AT6KEJLQZ` en canal `C0ARS4X5MF0` (#01-tareas-pendientes)
- Bot no tiene `groups:read` — solo listar canales publicos
- Ver [[slack-canvas-api-requiere-changes-array-con-operation]] y [[slack-bot-sin-groups-read-no-lista-canales-privados]]

## n8n API — credenciales no expuestas (2026-04-18)

`GET /api/v1/credentials` lista id/nombre/tipo pero nunca devuelve secrets. Guardar tokens fuera de n8n si se necesitan en otro contexto.
Ver [[n8n-api-publica-no-expone-valores-de-credenciales]]

## Migración masiva de workflows n8n vía script Python (2026-04-18)

Patrón para resetear N workflows desde JSONs originales con reemplazo de IDs:

1. Script Python lee JSONs originales + aplica `str.replace()` por cada par viejo→nuevo (credenciales, field_ids, pipeline, status, sub-workflow IDs, dominios, etc.)
2. Extrae solo campos válidos para la API: `name`, `nodes`, `connections`, `settings`, `staticData`
3. Guarda en `/tmp/cz_upload/` → sube con `PUT /api/v1/workflows/{id}`
4. Activar después con `POST /api/v1/workflows/{id}/activate`

Clave: los `field_id` en Code nodes van SIN comillas (`field_id: 337714`), necesitan reemplazo por separado de los que van como string.

Ver [[kommo-llt-requiere-subdominio-cuenta-no-api-c]] y [[n8n-debounce-redis-1s-causa-duplicados-en-chatbot]]

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

Cada org tiene su `phone_number_id` en `settings.whatsapp`. El webhook receptor busca org por ese ID.

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

## Obsidian vault sync via GitHub (2026-04-18)

Vault en `/Users/manueldelmonte/Obsidian/Manu/` sincronizado con `mdelmontep/obsidian-vault` (privado).
`/obsidian-1` hace push automático al final. Daily Briefing Manu lee de ahí cada mañana L-V 9:00.
Trigger ID: `trig_01THsqqvV3pg3WNnbgvkkdzk`
