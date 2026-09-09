---
title: partir el authorization server oauth obliga a mandar el iss (rfc 9207)
date: 2026-09-09
source: facturaia — conector MCP, login de Codex CLI (PR #2662)
tags: [oauth, mcp, rfc9207, rfc9700, codex, facturaia, gotcha]
---

Si el `authorization_endpoint` y el `issuer` viven en **orígenes distintos** (AS partido: consent en la app, `/token` en el servicio), un cliente que aplique la defensa anti-mix-up de **RFC 9700 §4.4** no puede atar el `code` que recibe a tu AS, y lo correcto por su parte es **negarse**. Codex lo hace en `codex-rs/rmcp-client/src/oauth/issuer_binding.rs`:

> OAuth authorization endpoint origin does not match the authorization server origin without issuer-bound callbacks

La condición literal que aborta: `origin(authorize) != origin(issuer) && origin(authorize) != origin(token) && authorization_response_iss_parameter_supported != true`. Con el AS partido las dos primeras se cumplen siempre, así que **RFC 9207 deja de ser opcional**.

Fix, y las dos piezas van en el **mismo despliegue** (anunciar sin mandar es peor que ninguna de las dos): `authorization_response_iss_parameter_supported: true` en el discovery **y** el `iss` en toda respuesta de `/authorize`, éxito y error. Orden: primero el que **manda** el `iss`, después el que lo **anuncia**.

Dos trampas de implementación: el `iss` se compara por **igualdad de cadena** con el `issuer` publicado (una barra final de más y falla), y el valor **crudo** del env puede ser el que firmas en el token — dos normalizaciones, dos funciones, una fuente. Hazlo parámetro **obligatorio** del builder del redirect y el typecheck impide olvidarlo en la ruta siguiente.

Falla **antes** del DCR, así que no deja rastro: cero filas del cliente en `oauth_clients` es la firma diagnóstica, no prueba de que el cliente no lo intentara. Ver [[el-puerto-del-redirect-de-loopback-no-cuenta-rfc-8252]] · [[mcp-connect-claude-origin-claude-com-y-aud-trailing-slash]].
