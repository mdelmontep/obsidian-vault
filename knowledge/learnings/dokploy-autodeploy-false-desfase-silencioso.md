---
title: dokploy compose con autodeploy=false acumula merges sin desplegar (desfase silencioso)
date: 2026-06-27
source: claude-code-session
tags: [dokploy, deploy, monitorizacion]
---
Un compose Dokploy con `autoDeploy=false` NO despliega los merges a main: el
servicio sigue sirviendo el build viejo y nadie se entera. Caso real: el MCP de
TuFacturaIA pasó 8 días con #453 (+30 tools) y #061 (fix seguridad) en main sin
desplegar; prod servía el build de 8 días antes.

No se pone a `true` porque redesplegaría en CADA push a main (la mayoría no toca
ese servicio) → recrea el contenedor → corta sesiones (fatal en un OAuth/MCP).
El churn es peor que el desfase.

Fix: GitHub Action con filtro de path (`paths:`) que llama a `compose.deploy`
SOLO cuando cambian los archivos del servicio. Red de seguridad sin CI:
manifiesto compartido + hash en `/health` que un sweep compara con main.
Verificar el deploy por comportamiento/`/health`, NUNCA por el `deployments[]`
de la API Dokploy (description cacheada >7 min → muestra commit viejo).

**Se repitió el 2026-07-27, y por eso el fix de arriba no basta.** El workflow con filtro de
paths (`deploy-mcp.yml`) es la mitigación correcta… pero vive en GitHub Actions, que lleva
40 días caído por billing. Resultado: tras el paso a Node 24 (#1257) el MCP siguió sirviendo
la imagen de Node 20, y solo se desplegó porque alguien lo comprobó a mano y lanzó
`POST /api/compose.deploy` con el `composeId` desde la API de Dokploy.

Regla: una mitigación alojada en la misma infra que puede caerse no es una mitigación, es
una intención. Si el deploy de un servicio depende de Actions, hace falta o bien una
comprobación de deriva desde fuera (hash de `/health` contra `main`), o bien acordarse de
desplegarlo a mano cada vez que se toca. Lo primero.

Deploy manual por API (sin panel): `curl -X POST .../api/compose.deploy -H "x-api-key: …"
-d '{"composeId":"…"}'`. Verificar SIEMPRE por comportamiento (`/health` con su hash de
tools), nunca por el `deployments[]`. Ver [[actions-sin-billing-hooks-locales-unico-gate]].

