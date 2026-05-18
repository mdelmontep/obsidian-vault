---
title: HTTP node n8n responseFormat=json revienta con 404 HTML de Traefik en redeploy
date: 2026-05-18
source: claude-code-session
tags: [n8n, dokploy, traefik, deploy, gotcha]
---

Durante ventanas de redeploy Dokploy, Traefik devuelve `404 page not found\n` (text/plain) brevemente. HTTP nodes con `responseFormat: 'json'` tiran "Response body is not valid JSON" antes de aplicar `neverError: true`.

Fixes según criticidad:
- Audit fire-and-forget → `responseFormat: 'text'` + `neverError: true`.
- Crítico → `options.retry: { tries: 3, waitBetweenTries: 1500 }`. Sobrevive ventanas <5s.

Ver [[n8n]] · [[docker-infra]]
