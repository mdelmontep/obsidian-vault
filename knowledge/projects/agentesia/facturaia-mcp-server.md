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
- **AS propio** con `@jmondi/oauth2-server` sobre Supabase Auth (sin bridge OIDC); auditoría de seguridad antes de prod.
- **Scopes finos** `*:read`/`*:draft`; `*:issue` NUNCA concedible. Permiso efectivo = rol ∩ scope.
- **Emisión fiscal por deep-link** (`app.tufacturaia.com/emitidas?factura={id}`), nunca tool autónoma. Ver [[acciones-irreversibles-no-tool-mcp-autonoma]].
- Multi-org: org activa sticky + tools `listar_empresas`/`seleccionar_empresa`.

## Estado por slice
- ✅ **041** contrato user-token JWT (ES256, valida `aud` RFC 8707, guard runtime de scope `:issue`).
- ✅ **044** v1 user-aware: `withApiV1` acepta api_key `fia_*` o user-token; `resolveV1Principal`+`authorizeV1Access` (puros, con TDD); 22 handlers migrados a `ctx.orgId/apiKeyId/userId/principal`; mig **326** `api_request_log.user_id`; escritura por user-token → 403 (fase).
- ✅ **043** mig **327** `oauth_server_tables`: `oauth_clients`(DCR) · `oauth_authorization_codes`(PKCE, 045) · `oauth_refresh_tokens`(`family_id`/`rotated_to`/`reused_at`, 046) · `oauth_events`(auditoría). Todas RLS service-role-only. **Se aplica a prod al mergear desde main** (no desde la rama).
- ✅ **042** skeleton transport en **`services/mcp-server/`** (patrón `pdf-renderer`). Streamable HTTP (SDK `@modelcontextprotocol/sdk` 1.29) + tool `whoami` (identidad cruda del dev-token, sin v1). Guards puros: flag `MCP_PUBLIC_ENABLED` off→endpoint+discovery mudos, dev-token solo fuera de prod, anti DNS-rebinding propio (el del SDK está deprecado). Corre como **ESM bajo tsx** (`tsconfig.mcp.json`; jose es ESM-only — ver [[jose-v6-esm-only-tsx-cjs-top-level-await]]). `Dockerfile.mcp`+`docker-compose.mcp.yml` = proyecto Dokploy aparte, `NODE_ENV=production` deja dev-token off. `dev/mint-token.ts` acuña par ES256+token para HITL. Test integración con cliente MCP real (empareja→listTools→whoami; sin auth→401). **2639/2639 tests, lint+typecheck verde.**
- ⏳ Resto = servicio Node separado: 045 AS core → 046 refresh/revoke → 047 gate seguridad → 048 oauth-real → 049 rol∩scope fino → 050/051 tools lectura → 052 multi-org → 053 crear-borrador+deep-link → 054 DCR/discovery → 055 consent → 056 rate-limit → 057 provider mcp-public → 058 docs → 059 auditoría+deploy. (060 analítica = Fase 2).

## Pendiente HITL / ops (no bloquea slices)
- Aplicar mig **327** a prod al mergear (verificar nº = primer hueco real al abrir PR).
- HITL skeleton: emparejar con cliente de header fijo (MCP Inspector o `claude mcp add --header "Authorization: Bearer <dev-token>"`) y correr `whoami`. El conector remoto de Claude.ai/ChatGPT exige OAuth → e2e completo en 048.

## Envs pendientes (cuando exista el AS)
Del servicio (042): `MCP_PUBLIC_ENABLED`, `MCP_ISSUER`, `MCP_AUDIENCE`, `MCP_ALLOWED_HOSTS`, `MCP_ALLOWED_ORIGINS`, `MCP_DEV_TOKEN_ENABLED`/`MCP_DEV_PUBLIC_KEY` (dev). Del AS (045+): firma privada ES256 + rotación de claves (JWKS).

## Continuar (pegar al arrancar)
> Continúo el MCP server de TuFacturaIA. Worktree `/Users/manueldelmonte/facturaia-mcp` (rama `feat/mcp-server`), no el repo principal. Lee `issues/mcp-server-prd.md` y `services/mcp-server/README.md`. Hechos+commiteados con TDD: 041, 044, 043 (mig 327 OAuth), 042 (skeleton transport + whoami en `services/mcp-server/`). Siguiente: issue **045** (authorization server core con `@jmondi/oauth2-server`: /authorize valida sesión Supabase + consent + emite user-token corto). TDD por slices, commit por slice. Antes: `cd /Users/manueldelmonte/facturaia-mcp && git log --oneline -8 && npm test`.
