---
title: Conectar un MCP remoto a Claude — 2 gotchas que rompen el connect (origin claude.com + aud trailing-slash)
date: 2026-06-19
source: debug E2E del conector MCP de TuFacturaIA (connect real desde claude.ai)
tags: [mcp, oauth, claude, rfc8707, facturaia, gotcha]
---

Al conectar el primer cliente REAL (Claude web) a nuestro servidor MCP remoto, el OAuth pasaba el consent pero fallaba después con "Authorization with the MCP server failed". El smoke server-side previo (curl con basura) NO lo cazó porque nunca hizo un exchange real ni mandó los headers de Claude. **Dos causas encadenadas:**

1. **Origin `claude.com`** — el backend del conector de Claude manda `Origin: https://claude.com` (Claude migró de claude.ai a claude.com). Nuestro `MCP_ALLOWED_ORIGINS` solo tenía `claude.ai,chatgpt.com` → el guard de origin del `/mcp` devolvía **403**. Fix: añadir `https://claude.com`. Ojo: el frontend sigue siendo claude.ai (el consent se ve), pero el backend que llama a `/token` y `/mcp` es claude.com.

2. **`aud` con barra final (RFC 8707)** — Claude manda `resource=https://mcp.tufacturaia.com/` (CON barra). El access token sale con `aud` con barra. La verificación (`jwtVerify` con `audience: expectedAud`) hace **match EXACTO** contra el valor configurado (sin barra) → rechaza → **401** → Claude entra en **bucle de refresh** (token_issued → N× token_refreshed en segundos → se rinde). Fix: normalizar la barra final y aceptar ambas formas (`aud` y `aud/`) en `verifyUserToken` (afecta `/mcp` y `/api/v1`, que la comparten).

**Cómo diagnosticarlo sin logs** (el servicio solo logueaba el arranque): reproducir el flujo OAuth COMPLETO con Playwright (login → authorize → consent → capturar el `code` del header Location del 303 → POST `/token` → `/mcp` initialize/tools/call) **mandando los headers exactos de Claude** (Origin claude.com, resource con barra). Y consultar la BD: `oauth_refresh_tokens.resource` revela el `resource` exacto que mandó el cliente; el patrón `token_issued`+N×`token_refreshed` en segundos = bucle de refresh = /mcp rechaza el token.

Datos: redirect_uri de Claude = `https://claude.ai/api/mcp/auth_callback`. PRs #385 (aud) + #386 (origin default). Ver [[mcp-conector-remoto-limites-claude-chatgpt-cursor]].
