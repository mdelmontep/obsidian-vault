---
title: n8n compose con networks external true falla en dokploy nuevos
date: 2026-05-22
source: claude-code-session
tags: [n8n, docker, dokploy, deploy]
---

Compose con `networks.X.external: true` falla al deploy con `network X not found` en Dokploy nuevos (caso EcoBox: Stackscale Docker no-Swarm).

El Dokploy AgentesIA viejo SÍ pre-crea la network antes de `docker compose up`, así que en compose copiados de Danny/CZ funciona con `external: true`. En Dokploy fresh esa pre-creación no existe.

Fix: **quitar `external: true`** (o dejar `external: false`). docker-compose la crea solo.

Diagnóstico rápido: status `error` + container `state=created` + error en docker inspect:
```
failed to set up container networking: Could not attach to network X: rpc error: code = NotFound desc = network X not found
```

Caso real: EcoBox 2026-05 — stack `ecobox-n8n-rniwbw` no arrancó hasta quitar `external: true` del compose.
