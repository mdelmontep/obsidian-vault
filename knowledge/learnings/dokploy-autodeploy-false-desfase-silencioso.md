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
