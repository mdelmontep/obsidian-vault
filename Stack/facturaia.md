---
title: TuFacturaIA — stack, gotchas y operación
date: 2026-05-19
source: claude-code-session
tags: [facturaia, stack, supabase, verifactu, aeat]
---

# TuFacturaIA

SaaS de facturación con envío a AEAT vía Verifactu. Repo: `/Users/manueldelmonte/facturaia/` · remote `git@github.com:AgentesIA-MAdrid/facturaia.git`.

## Infra crítica

| Qué | Valor |
|---|---|
| Dominio activo | `https://app.tufacturaia.com` |
| Dominio antiguo (caído, 404) | `~~facturaia.agentesia.world~~` |
| Prefijo API | `/api/v1/*` (no `/v1/*`) |
| BD Supabase | proyecto `lahqlyaxvobqjgdiftag` — **misma BD** que servía el dominio antiguo |
| Org AgentesIA Lab SL | `ea201784-4813-4eae-ac3f-9cffdb9cc24a`, NIF B27602085 |
| Mapping ↔ agency-portal | `agency_id 75fe4392-…` ↔ esa org. Guardado en `agency-portal.facturaia_org_agency_map` |

El cliente HTTP del portal añade `/api/v1` automáticamente (`src/lib/facturaia/client.ts:43`). En `.env.local` poner solo el host: `FACTURAIA_API_URL=https://app.tufacturaia.com`.

**Mapping client portal ↔ cliente_remote_id FacturaIA** vive en `agency-portal/src/lib/facturaia/tenant-cliente-mapping.ts` (`resolveTenantClienteRemoteIds`). Dos fuentes: `prospects.facturaia_cliente_id` + `cliente_remote_id` de sombras enlazadas a `agency_invoices`/`invoices`/`quotes` del tenant. Consumido por listado tenant y por proxy PDF (single source of truth). Ver [[ADR-023-mapping-client-portal-cliente-remote-id-facturaia]].

## Convenciones del repo

- App Router (Next.js). Route Handlers, **no** Server Actions para mutaciones.
- Pipeline canónico: `withApiAuth({ endpoint, parseBody, rateLimit, requireRole: ['propietario','admin'] }, async ({ orgId, userId, body }) => {…})` (`src/lib/api/with-api-auth.ts`).
- Roles: `propietario`, `admin`, `contable`, `comercial`, `gestor_externo`, `solo_lectura` (`src/lib/auth/actor.ts` → `ORG_ROLES`).
- Super-admin: dos mecanismos — env `SUPERADMIN_EMAILS` **o** flag `profiles.is_superadmin=true`. Solo el flag de BD es accesible desde triggers SQL.
- Cliente HTTP cliente: `supabase` con anon key + cookie de sesión (RLS). Backend usa `createAdminClient()` (service_role) tras validar rol en `withApiAuth`.
- `audit_log` table (`001_schema.sql`) — todas las mutaciones críticas escriben aquí. Schema: `org_id, user_id, accion, entidad, entidad_id, detalles jsonb, ip`.

## Gotchas operativos

### Toggle Verifactu — PR #48 (mig 095)

El toggle "Verifactu" en Settings → Fiscal vivía en `settings.fiscal.verifactu` (JSON) Y en `organizations.verifactu_activo` (columna). El JSON era huérfano — todo el sistema (worker, triggers, gating módulo, PDFs, voz) leía la columna. UI escribía ambos pero con bug: si el JSON no tenía la clave (`undefined`) y la columna era `false`, el siguiente "Guardar" reactivaba silenciosamente Verifactu.

**Fix mergeado 2026-05-19** (`origin/main` commit `188f519`):
- Fuente única: `organizations.verifactu_activo`. JSON purgado por la migración 095.
- API `PUT /api/settings/verifactu` con `requireRole:['propietario','admin']` + Zod.
- Trigger `BEFORE UPDATE guard_verifactu_settings` rechaza mutación si el caller no es owner/admin/superadmin (defensa en profundidad — la policy `org_member_update` permite a cualquier miembro UPDATE, vulnerable hasta el trigger).
- Trigger `AFTER UPDATE audit_verifactu_settings_change` inserta en `audit_log` con `user_id`, IP, UA, old/new.

Pendiente: Fase 3 UX (dirty pill, disabled sin cert .p12, warning con facturas en cola) + Fase 4 a11y (`SettingsToggle` → `role=switch`).

### Vulnerabilidad latente — `org_member_update` policy

`supabase/migrations/003_missing_tables_and_policies.sql:32` deja UPDATE de `organizations` a cualquier miembro (sin distinguir rol). Para Verifactu lo mitigamos con trigger. **Otras columnas regulatorias podrían tener el mismo problema** (revisar antes de exponerlas en UI). Candidatos a revisar: `regimen_iva`, `iae`, `nif`, `verifactu_num_instalacion`.

### Verifactu `pendiente_envio` colgadas si apagas Verifactu

`api/verifactu/process/route.ts:31` filtra por `.eq('verifactu_activo', true)`. Si apagas el toggle con facturas en cola, quedan `pendiente_envio` indefinidamente. No es regresión del fix nuevo — comportamiento preexistente. Pendiente: job de cleanup que las marque `no_aplica` o warning UX antes de apagar.

### `api_idempotency` queda stale tras wipe

Si se borran facturas/presupuestos en `cuenta a 0`, las idempotency keys en `api_idempotency` siguen apuntando a IDs ya borrados. Reutilizar la misma `Idempotency-Key` devuelve la respuesta cacheada (24h TTL). **Limpiar antes de re-emitir**: `DELETE FROM api_idempotency WHERE org_id='…'`.

### Tres cuentas gh CLI — switch antes de tocar TuFacturaIA

`gh` está logueado con `mdelmonteagentesia` (default), `AgentesIAMadrid` y `mdelmontep`. La default NO tiene acceso al repo TuFacturaIA → `gh api repos/AgentesIA-MAdrid/facturaia` da 404. Antes de PR/merge:
```bash
gh auth switch -u AgentesIAMadrid
```
Para `git push` da igual la cuenta gh — usa SSH key.

## Operaciones comunes

### Aplicar migración

```bash
cd ~/facturaia && supabase db push
```
o vía MCP `mcp__supabase__apply_migration` (project_id `lahqlyaxvobqjgdiftag`).

### Workflow PR limpio cuando `main` local diverge de `origin/main`

```bash
cd ~/facturaia
git worktree add .worktrees/my-fix origin/main -b fix/my-branch
# copiar archivos al worktree, commit, push
gh pr create --base main --head fix/my-branch
gh pr merge <num> --squash --delete-branch
git worktree remove .worktrees/my-fix
```

### Reset cuenta a 0 (cuidado — irreversible)

Orden por FK (ver [[2026-05-18-facturaia-reset-agentesia]]):
1. `DELETE FROM bandeja_ingesta`
2. `DELETE FROM cobros_recordatorios`
3. `DELETE FROM facturas` (cascadea `lineas_factura`)
4. `DELETE FROM presupuestos`
5. `DELETE FROM clientes` (cascadea `clientes_opt_out`)
6. `UPDATE series_numeracion SET contador_actual=0`
7. En portal: `DELETE FROM facturaia_documents WHERE agency_id='…'`

**Validar antes:** `SELECT verifactu_estado, COUNT(*) FROM facturas WHERE org_id='…' GROUP BY 1`. Si alguna está `enviada_aceptada` o equivalente → NO BORRAR sin rectificativa AEAT.

## Triggers / RPCs SQL relevantes

- `trigger_verifactu_huella()` (mig 015/085/089/091) — calcula encadenado huella SHA-256 cuando se INSERTa/UPDATEa una factura con `verifactu_activo`. Lock advisory por (org,serie) para evitar race.
- `guard_verifactu_settings()` (mig 095) — BEFORE UPDATE organizations, rechaza cambio Verifactu/entorno si rol insuficiente.
- `audit_verifactu_settings_change()` (mig 095) — AFTER UPDATE organizations, escribe a `audit_log` con `request.headers` para IP/UA.
- `create_factura_with_lineas` RPC (mig 094, work-in-progress 2026-05-18) — INSERT atómico factura+líneas para cerrar race A-fiscal.
- **Guard revert persistente** (mig 128, 2026-05-20) — `facturas.last_revert_at TIMESTAMPTZ` seteado por `detect_reembolso_for_cobro` (117) y `detect_reembolso_movimiento` (112) en el UPDATE de revert. Filtrado `IS NULL OR < NOW() - INTERVAL '30 days'` en 4 funciones de auto-match (`auto_mark_cobradas_on_movimiento_emitidas` 114, `auto_mark_pagadas_on_movimiento` 112, `auto_mark_cobrada_on_bank_match` 117, `auto_mark_pagada_on_bank_match` 111). Sin esto un +mov casual del mismo importe re-cobraba silenciosamente tras devolución (caso real bug fiscal: [[postgres-guard-transition-no-persiste-en-recompute-chain]]).

## Multi-org canónico (mig 120-127, 2026-05-20)

- **Fuente única**: `profiles.active_org_id` (mig 120, FK org ON DELETE SET NULL). `get_user_org_id()` SQL y `resolveActiveOrg` TS comparten path (active_org_id + fallback `invited_at ASC` + writeback). Ver [[rls-multi-tenant-limit-1-sin-order-bug-latente]].
- **Matriz permisos rol-aware**: función SQL `user_can_write_in_org(p_org_id, p_resource)` (mig 121+123+127) — single source of truth. Espejo TS `src/lib/auth/role-matrix.ts`. Aplicada en RLS de 14 tablas core + `withApiAuth.requireWrite`. **Modificar = tocar AMBOS** (SQL + TS) + test vitest. Ver [[matriz-permisos-rol-aware-bd-mas-espejo-ts]] + [[ADR-008-matriz-permisos-rol-aware-bd]].
- **`/sin-acceso` fallback**: user con JWT vivo sin org operable (revocado/expirado) → página con mensaje + logout limpio. NO redirigir a `/login` (loop con middleware). Ver [[ADR-007-sin-acceso-fallback-vs-loop-redirect]] + [[signOut-solo-invalida-refresh-no-access-token]].
- **Bot WhatsApp sticky multi-org** (mig 125): `whatsapp_org_selection` PK user_id, TTL 6h sliding (24h si source=`web_switch`). Resolver: N=1 directo · sticky viva · `active_org_id` + upsert · sino `multi_org_pendiente` con candidates para workflow n8n.
- **Lifecycle equipo**: invitar = `createUser` → INSERT membership → `generateLink` → email Resend → rollback (`deleteUser` + delete membership) si falla. Ver [[supabase-createuser-race-trigger-handle-new-user]]. Soft delete (`estado='revocado'` + `revoked_at` + `signOut('global')` + limpiar sticky). Cron `team-expire-invites` pasa `invitado→expirado` tras 30d (con `revoked_at=now()` para CHECK mig 126).

## Modelo invitación consent-explícito (mig 129/130, 2026-05-21)

- **TODA invitación = `estado='invitado'`** (no más rama "existing user → activo directo"). Email único `team-invite-email` con link "Aceptar invitación a [Org]". Ver [[ADR-009-invitacion-consent-explicito-vs-activo-directo]].
- **Endpoint `POST /api/team/invitations/accept`** — el invitado promueve su propia membership `invitado → activo`. Bypass OTP gate (acepto antes de verificar phone). Limpia `revoked_at + expires_at` por CHECK mig 126.
- **Page `/invitacion`** — público en middleware (path `isAuthPage` + bypass redirect-si-autenticado). Bifurcada por edad del user: <60s → set password + auto-accept, >60s → botón Aceptar. Detecta hash `#error=otp_expired` para UX claro. Ver [[hash-magic-link-supabase-requiere-setsession-explicito]].
- **Mig 129** — RLS `org_members_select` ampliada `OR user_id = auth.uid()`: invitado puede leer su propia fila pending en orgs distintas a su `active_org_id`. Ver [[rls-org-members-select-debe-incluir-own-memberships]].
- **Mig 130** — trigger `handle_new_user` perdió rama legacy `invited_to_org_id`. Antes duplicaba el INSERT del endpoint con `estado='activo'` → UNIQUE violation. Ver [[trigger-handle_new_user-rama-legacy-choca-con-insert-explicito]].
- **Cookie `impersonate_org` confinada a `/admin/*`** — fuera de ese path el proxy borra del `request.cookies` (no solo response) para que handlers no resuelvan orgId al valor impersonado. Ver [[cookie-impersonate-leak-fuera-de-admin]].
- **`siteUrl` con fallback header** — endpoints accept/invite aceptan `NEXT_PUBLIC_SITE_URL || NEXT_PUBLIC_APP_URL || x-forwarded-host` (Dokploy a veces no propaga envs runtime). Ver [[next-public-envs-dokploy-runtime-fallback-headers]].

## Bot WhatsApp conversacional + cambio org (PR-Bot-1.x/2.x, 2026-05-21)

- Workflow n8n `pqSWkDIHqmSVHotB` (`n8n.tufacturaia.com`). 10 patches encadenados idempotentes en `n8n/patches/apply-pr-bot-*.py` con markers `PR_BOT_1` → `PR_BOT_2_5`. Snapshots staged en `n8n/workflows/staged/`.
- Tono colega contable + tipo `conversacion` para small_talk → texto plano sin 🧾. Bloque `<context>` en chatInput: `IS_FIRST_TIME`, `STICKY_ORG_NAME`, `HAS_MULTI_ORG`, `CANDIDATE_ORGS`.
- Cambio org desde chat: agente devuelve `cambio_org_solicitado` con `target_org_id` (si match inequívoco → bypass lista; si ambiguo → WhatsApp Interactive List nativa). Router temprano `Es Org Select?` + POST `select-org` + reply "Cambiado a X. Repite tu mensaje". v1 dos turnos sin reprocesado, ver [[ADR-011-bot-whatsapp-org-switch-v1-dos-turnos-vs-reprocesado]].
- Defensa en código en `Parsear y Calcular Totales`: invariantes (precio>0, NIF presente en factura) validados aquí, no en prompt. Ver [[defensa-en-codigo-vs-prompt-llm-para-invariantes-de-dominio]].

## Validación NIF (`src/lib/validation/spanish-tax-id.ts`)

- `validateSpanishTaxId()` cubre los 3 algoritmos (DNI módulo 23, NIE con sustitución X/Y/Z, CIF suma pares+impares según letra inicial). 17 tests vitest. Ver [[nif-espana-paraguas-dni-nie-cif-desde-rd-1065-2007]].
- **Helper REPLICADO en n8n** (Code node de `Parsear y Calcular Totales`). Si cambias el algoritmo aquí, refleja allí (no hay import).
- Copy en mensajes mantenido como "NIF" genérico (cubre los 3). "CIF/NIF" si B2B explícito.

## Links

- Reset 2026-05-18: ver memoria `agentesia-org-reset-2026-05-18` (auto-memory agency-portal)
- Decisión particular FACT-2026-0001: ver memoria `fact-2026-0001-particular`
- Infra recap: ver memoria `facturaia-infra`

## Rescatados de hot.md (poda 2026-06-02)

- **Verifactu huella NO incluye conceptos/descripciones** — solo NIF+Num+Fecha+TipoFactura+CuotaTotal+ImporteTotal+Huella_ant (mig 091:122-128). Añadir/quitar campos textuales a `lineas_factura` es seguro retroactivamente, no rompe cadena AEAT.
- **Recrear RPC entero al añadir campo a INSERT con columnas explícitas** — `CREATE OR REPLACE` reemplaza la función completa, no parchea. Copiar versión vigente byte-a-byte + insertar campo nuevo.
- **fecha_cobro/fecha_pago = mb.fecha NUNCA CURRENT_DATE** — criterio caja AEAT IVA exige fecha del movimiento, no de la inserción del registro. Mig 111 fix retroactivo a 4 triggers.
- **UI lista no filtraba `deleted_at`** — comentario decía "defensivo por mig 106 no aplicada", llevaba semanas aplicada. Coste: movs soft-deleted seguían apareciendo. Auditar comentarios "defensivos" caducados al deployar la mig que cubren.
- **CSV import `imported:0` con error oculto en UI** — log warn en endpoint cuando `parsed.movimientos.length === 0` o errors no vacíos. UI muestra solo 3 campos; warnings se perdían. Defense: console.warn server-side + Network preview DevTools.
