---
title: FacturaIA — stack, gotchas y operación
date: 2026-05-19
source: claude-code-session
tags: [facturaia, stack, supabase, verifactu, aeat]
---

# FacturaIA

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

### Tres cuentas gh CLI — switch antes de tocar FacturaIA

`gh` está logueado con `mdelmonteagentesia` (default), `AgentesIAMadrid` y `mdelmontep`. La default NO tiene acceso al repo FacturaIA → `gh api repos/AgentesIA-MAdrid/facturaia` da 404. Antes de PR/merge:
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
- **Lifecycle equipo**: invitar = `createUser` → INSERT membership → `generateLink` → email Resend → rollback (`deleteUser` + delete membership) si falla. Ver [[supabase-createuser-race-trigger-handle-new-user]]. Soft delete (`estado='revocado'` + `revoked_at` + `signOut('global')` + limpiar sticky). Cron `team-expire-invites` pasa `invitado→expirado` tras 30d.

## Links

- Reset 2026-05-18: ver memoria `agentesia-org-reset-2026-05-18` (auto-memory agency-portal)
- Decisión particular FACT-2026-0001: ver memoria `fact-2026-0001-particular`
- Infra recap: ver memoria `facturaia-infra`
