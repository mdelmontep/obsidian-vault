---
title: conectores mcp remotos exigen oauth 2.1, no api key estática
date: 2026-06-18
source: claude-code-session
tags: [mcp, oauth, anthropic, integraciones]
---
Los conectores MCP **remotos** de Claude (web/CLI) y ChatGPT exigen **OAuth 2.1**; no aceptan una API key estática pegada a mano. La spec MCP (2025) hizo OAuth obligatorio para remote servers: el MCP server actúa como *resource server* y un *authorization server* emite los tokens (transport Streamable HTTP + DCR RFC 7591 + discovery RFC 8414/9728 + PKCE).

La API key cruda solo sirve para MCP **local** (stdio): clonar repo + `npm i` + key en `.mcp.json` (el modelo de los wrappers de terceros, p.ej. Holded). Para un SaaS con conector remoto "Añadir → login → conectado", hay que montar OAuth sí o sí.

No hace falta construir el IdP entero: hay AS gestionados (WorkOS AuthKit, Scalekit) con "bring your own auth", o `@jmondi/oauth2-server` (~300 LOC) sobre tu auth existente (caso TuFacturaIA, ver [[facturaia-mcp-server]]).
