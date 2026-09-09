---
title: el puerto del redirect de loopback no cuenta (rfc 8252 §7.3)
date: 2026-09-09
source: facturaia — conector MCP, login de Codex CLI (PR #2662)
tags: [oauth, rfc8252, cli, redirect-uri, facturaia, gotcha]
---

Un cliente nativo (CLI de Codex, `codex mcp login`) registra su callback **sin puerto** —`http://127.0.0.1/callback/<id>`— y autoriza con el **puerto efímero** que le da el SO al listener, distinto en cada intento. Con `redirect_uri` por igualdad estricta, el **segundo login funciona nunca**: el primero pasa por casualidad si el puerto coincide, el resto se van con `invalid_request`.

RFC 8252 §7.3 lo dice explícito: el AS «MUST allow any port to be specified at the time of the request for loopback IP redirect URIs». La excepción es **solo del puerto** y **solo para IPs de loopback** (`127.0.0.1`, `[::1]`): esquema, host, path, query y fragmento siguen comparándose enteros. **`localhost` queda fuera** — §8.3 desaconseja el nombre porque puede resolver a una interfaz que no es la máquina local, y ahí aflojar sí amplía superficie.

El test que importa no es el que acepta, es el que **sigue rechazando**: `localhost` con puerto, mismo loopback con otro path, y origen ajeno. Prueba a **aflojar** la lista (meter `localhost`) y comprueba que un test muere; si no muere, el candado no existe.

Y para verificarlo contra prod hace falta **sesión**: sin ella `/authorize` redirige a login *antes* de validar el `redirect_uri`, así que los cinco casos —incluidos los que deben fallar— dan verde y el chequeo no discrimina nada.

Ver [[partir-el-authorization-server-oauth-obliga-a-mandar-el-iss]] · [[un-control-negativo-que-no-discrimina-invalida-el-test-entero]].
