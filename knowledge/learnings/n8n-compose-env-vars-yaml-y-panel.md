---
title: dokploy compose pasa al container solo las env listadas en el yaml, no las del panel
date: 2026-05-30
source: claude-code-session
tags: [dokploy, n8n, infra, env]
---

Dokploy `compose.environment:` del docker-compose.yml es la lista exacta de envs que se inyectan al container. Lo que añades por panel UI (`env:` de Dokploy) son solo VALORES — el YAML decide qué se exporta. Si la var nueva no está como `- VAR=${VAR}` en el YAML, el container no la ve.

Caso 2026-05-30: `FACTURAIA_SIGNING_SECRET` plantado en panel + `compose.deploy` → workflow temporal n8n reportaba `has_signing_secret:false`. Fix: editar `composeFile` añadiendo `- FACTURAIA_SIGNING_SECRET=${FACTURAIA_SIGNING_SECRET}` al `environment:` block + re-deploy. Misma trampa con `NODE_FUNCTION_ALLOW_BUILTIN`.

Antes de añadir env nueva en Dokploy con compose YAML editado a mano: editar AMBOS sitios (panel + composeFile).
