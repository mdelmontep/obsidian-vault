---
title: facturaia-mcp-server
date: 2026-06-18
tags: [facturaia, mcp, oauth, api-v1]
---

# TuFacturaIA — MCP server remoto (estado + continuación)

Servidor MCP oficial en `mcp.tufacturaia.com`: conecta TuFacturaIA a Claude/ChatGPT/Cursor para leer datos y **preparar** borradores en lenguaje natural. Wrapper **OAuth 2.1 user-level** sobre la API v1 existente. Sustituye el diseño previo `auth_type='mcp'` con API key (solo servía para MCP local, modelo Holded de terceros).

## Dónde
- Worktree `/Users/manueldelmonte/facturaia-mcp` · rama `feat/mcp-server` (desde `origin/main`).
- PRD + 20 issues: `issues/mcp-server-prd.md` + `issues/041-060`.

## Decisiones (grill + 3 agentes)
- **Servicio Node separado** en `mcp.tufacturaia.com` (Dokploy), Streamable HTTP, llama a la v1 por HTTP.
- **Identidad user-level** (no api_key org-level): el token lleva user+orgs; audita a nombre del usuario (`actor_type='agent:mcp'`).
- **Enforcement en la v1** (user-aware) reutilizando el `role-matrix` **TS** (`canWriteInOrg`) — NO la SQL `user_can_write_in_org` (usa `auth.uid()`, null bajo service_role). Ver [[funcion-sql-auth-uid-no-invocable-desde-service-role]] si se crea.
- **AS propio** sobre Supabase Auth (sin bridge OIDC); auditoría de seguridad antes de prod.
- **(2026-06-18) Sesión OAuth = split app↔servicio (Opción A).** `/authorize`+consent como rutas Next en `app.tufacturaia.com` (reusa la sesión Supabase ya presente, no toca cookies; mina el auth code en `oauth_authorization_codes`). `/token`+JWKS+discovery en el servicio MCP. Cookie en dominio padre descartada (tocaba la config del app en prod).
- **Replantear `@jmondi/oauth2-server`**: con el AS partido en 2 procesos, la lib (AS de un solo proceso) encaja mal. Recomendación: hand-roll usando las tablas 043 + validadores 045a (`policy.ts`) + contrato 041, con tests negativos. PENDIENTE confirmar (es decisión PRD-level).
- **Scopes finos** `*:read`/`*:draft`; `*:issue` NUNCA concedible. Permiso efectivo = rol ∩ scope.
- **Emisión fiscal por deep-link** (`app.tufacturaia.com/emitidas?factura={id}`), nunca tool autónoma. Ver [[acciones-irreversibles-no-tool-mcp-autonoma]].
- Multi-org: org activa sticky + tools `listar_empresas`/`seleccionar_empresa`.

## Estado por slice
- ✅ **041** contrato user-token JWT (ES256, valida `aud` RFC 8707, guard runtime de scope `:issue`).
- ✅ **044** v1 user-aware: `withApiV1` acepta api_key `fia_*` o user-token; `resolveV1Principal`+`authorizeV1Access` (puros, con TDD); 22 handlers migrados a `ctx.orgId/apiKeyId/userId/principal`; mig **326** `api_request_log.user_id`; escritura por user-token → 403 (fase).
- ✅ **043** mig **327** `oauth_server_tables`: `oauth_clients`(DCR) · `oauth_authorization_codes`(PKCE, 045) · `oauth_refresh_tokens`(`family_id`/`rotated_to`/`reused_at`, 046) · `oauth_events`(auditoría). Todas RLS service-role-only. **Se aplica a prod al mergear desde main** (no desde la rama).
- ✅ **042** skeleton transport en **`services/mcp-server/`** (patrón `pdf-renderer`). Streamable HTTP (SDK `@modelcontextprotocol/sdk` 1.29) + tool `whoami` (identidad cruda del dev-token, sin v1). Guards puros: flag `MCP_PUBLIC_ENABLED` off→endpoint+discovery mudos, dev-token solo fuera de prod, anti DNS-rebinding propio (el del SDK está deprecado). Corre como **ESM bajo tsx** (`tsconfig.mcp.json`; jose es ESM-only — ver [[jose-v6-esm-only-tsx-cjs-top-level-await]]). `Dockerfile.mcp`+`docker-compose.mcp.yml` = proyecto Dokploy aparte, `NODE_ENV=production` deja dev-token off. `dev/mint-token.ts` acuña par ES256+token para HITL. Test integración con cliente MCP real (empareja→listTools→whoami; sin auth→401). **2639/2639 tests, lint+typecheck verde.**
- ✅ **045 AS OAuth core COMPLETO** (hand-roll, ADR-032; src/lib/oauth compartido app↔servicio):
  - 045a validadores puros (`oauth/policy.ts`): scope allowlist (`:issue` no concedible), PKCE S256 obligatorio + `verifyPkceS256` (RFC 7636), redirect_uri match EXACTO, state. Test negativo por criterio.
  - 045b base pura: `crypto.ts` (opaco+sha256), `authorize-request.ts` (resolveClientRedirect aparte — no redirige errores a URI no validada — + validateAuthorizeParams scope∩cliente), `exchange.ts` (validateCodeExchange → invalid_grant), `store.ts` (adaptador BD inyectado), `issue-code.ts`, `redirects.ts`, `token.ts` (issueTokensForGrant firma 041), `exchange-flow.ts` (orquesta canje, consumo atómico=replay guard).
  - 045c `/authorize`+consent en el app (`src/app/oauth/authorize` + `POST /api/oauth/consent`): sesión Supabase, re-valida todo server-side (identidad de la sesión, no del form), mina code (hash en BD) service-role, audita.
  - 045d `/token` en el servicio (`token-endpoint.ts`+`server.ts`): canje → user-token 041 real verificable + refresh; rate-limit+lockout en memoria, Cache-Control no-store, 405/503; deps reales desde Supabase service-role. Test integración HTTP: canje→token verificable, single-use, 405.
  - **lint+typecheck+build verde.** Pendiente menor: rate-limit en `/authorize` (hoy session-gated; añadir al pulir/047).
- ✅ **046 refresh + revocación** (`refresh-flow.ts` puro + store): token 041 gana claim `gid` (=familia). `grant_type=refresh_token` rota (uno por uso); presentar un refresh ya rotado/revocado = reúso → revoca la FAMILIA entera; guard atómico de carrera. `POST /revoke` (RFC 7009, por posesión). Store: getRefreshByHash, markRefreshRotated (UPDATE atómico), revokeFamily, isGrantRevoked, getFamilyByRefreshHash.
- ✅ **048 resource server con OAuth real** (`authenticateResource`): whoami verifica el user-token contra cadena de claves (prod=pública AS; dev-token solo en dev) y rechaza si el grant (gid) está revocado, sin esperar a exp; fail-closed sin backend de revocación. **2715+ tests, todo verde.**
- ✅ **047 GATE auditoría seguridad** — 4 revisores independientes + síntesis. **0 P0.** Fixes aplicados: anti-rebinding en `/token`+`/revoke` (era CSRF-able), revocación DURABLE (tabla `oauth_revoked_grants` mig **328** — antes `isGrantRevoked` dependía de filas de refresh), formato code_challenge (RFC 7636), guard `reused_at`, `error_description` genérico, IP en consent, cache clave. **E2E cadena completa** (`oauth-e2e.test`: token→whoami→refresh→revoke→rechazo→reúso). Registro: `services/mcp-server/SECURITY-AUDIT-047.md` (gate BLOQUEANTE de 050+, **pendiente firma humana**). Diferido → issues **061** (idempotencia rotación, FK), **062** (rate-limit compartido + clientIp), **063** (guardarraíl detail jsonb). 2721 tests verde.
- ⏳ Resto: **firma humana del gate 047** → 049 rol∩scope fino → 050/051 tools lectura → 052 multi-org → 053 crear-borrador+deep-link → 054 DCR/discovery → 055 consent pulido → 056 rate-limit/idempotency tools (atar #061/#062) → 057 provider mcp-public → 058 docs → 059 deploy (crear proyecto Dokploy mcp.tufacturaia.com + DNS). (060 Fase 2).

## Pendiente HITL / ops (acción de Manu)
- **Generar par ES256 del AS** (openssl en `.env.example`): privada → `MCP_SIGNING_PRIVATE_KEY` (servicio); pública → `MCP_USER_TOKEN_PUBLIC_KEY` (app, la v1 verifica). Sin la privada, `/token` da 503.
- **Supabase env en el contenedor MCP**: `NEXT_PUBLIC_SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY` (ya en `docker-compose.mcp.yml`).
- Aplicar mig **327** a prod al mergear (verificar nº primer hueco al abrir PR).
- **047: auditoría de seguridad humana del flujo OAuth ANTES de exponer** (flag `MCP_PUBLIC_ENABLED` sigue off).
- HITL: emparejar con MCP Inspector / `claude mcp add --header`. Conector remoto Claude.ai exige OAuth → e2e completo tras 048.

## Continuar (pegar al arrancar)
> Continúo el MCP server de TuFacturaIA. Worktree `/Users/manueldelmonte/facturaia-mcp` (rama `feat/mcp-server`). Lee `issues/mcp-server-prd.md`, `services/mcp-server/README.md`, `[[facturaia-mcp-server]]` y `[[ADR-032-mcp-oauth-as-split-app-servicio-handroll]]`. **Núcleo OAuth COMPLETO+TDD**: 041, 044, 043 (mig 327), 042 (skeleton), 045 (/authorize+consent app + /token servicio → user-token 041), 046 (refresh rotación/reúso/revocación + /revoke + claim gid), 048 (resource server verifica AS + corta grant revocado). Falta el **gate 047 (auditoría seguridad humana) antes de exponer**, y feature work 049-059. Siguiente código: **049** (permiso efectivo = rol ∩ scope: re-resolver rol por (user,org) server-side y cruzar con el scope del token) o **050/051** (tools de lectura de facturas/resto sobre la v1 user-aware). TDD por slices. Antes: `cd /Users/manueldelmonte/facturaia-mcp && git log --oneline -12 && npm test`.
