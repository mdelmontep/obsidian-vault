---
title: dokploy compose con autoDeploy=false no recibe los merges a main
date: 2026-06-19
source: claude-code-session
tags: [dokploy, deploy, facturaia]
---
En el proyecto Dokploy `tufacturaia-prod` solo el compose `tufacturaia-app` tiene `autoDeploy=true`; `mcp-server` (composeId `pvUJ67f8qdLKOitI8RERO`) y `ticket-runner` están en `autoDeploy=false`. Consecuencia: mergear a main NO actualiza esos contenedores — siguen sirviendo código viejo indefinidamente (el MCP estuvo ~1 día atrás, sin las tools de #409).

Tras mergear algo que afecte a un servicio con `autoDeploy=false` hay que disparar `POST /api/compose.deploy {composeId}` a mano. Verificar el flag por servicio: `project.one` → `environments[].compose[].autoDeploy`.

Combinar con [[dokploy-api-deployments-sin-ordenar]]: el `deployments[]` no viene ordenado por fecha → no fiarse de `[0]` para confirmar el commit desplegado; buscar el deploy por SHA en todo el array.
