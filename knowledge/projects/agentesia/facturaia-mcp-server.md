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
- ✅ **044** v1 user-aware: `withApiV1` acepta api_key `fia_*` o user-token; `resolveV1Principal`+`authorizeV1Access` (puros, con TDD); 22 handlers migrados a `ctx.orgId/apiKeyId/userId/principal`; mig **326** `api_request_log.user_id`; escritura por user-token → 403 (fase). **2613/2613 tests, typecheck+lint limpios.**
- ⏳ Resto = servicio Node separado: 043 migración OAuth → 042 skeleton → 045 AS core → 046 refresh/revoke → 047 gate seguridad → 048 oauth-real → 049 rol∩scope fino → 050/051 tools lectura → 052 multi-org → 053 crear-borrador+deep-link → 054 DCR/discovery → 055 consent → 056 rate-limit → 057 provider mcp-public → 058 docs → 059 auditoría+deploy. (060 analítica = Fase 2).

## Envs pendientes (cuando exista el AS)
`MCP_USER_TOKEN_PUBLIC_KEY` (SPKI/PEM, pública ES256 del AS), `MCP_OAUTH_ISSUER`, `MCP_RESOURCE_AUDIENCE`.

## Continuar (pegar al arrancar)
> Continúo el MCP server de TuFacturaIA. Worktree `/Users/manueldelmonte/facturaia-mcp` (rama `feat/mcp-server`), no el repo principal. Lee `issues/mcp-server-prd.md`. Hechos+commiteados con TDD: 041 y 044. Siguiente: montar el servicio MCP Node separado empezando por issue **043** (migración OAuth) y **042** (skeleton + `whoami`). TDD por slices, commit por slice. Antes: `cd /Users/manueldelmonte/facturaia-mcp && git log --oneline -5 && npm test`.
