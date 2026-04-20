---
title: facturaia deploy automatico dokploy
date: 2026-04-20
source: claude-code-session
tags: [facturaia, dokploy, pendiente]
---

Dokploy no auto-deploya al push a GitHub. Actualmente requiere deploy manual desde el dashboard de Dokploy + reload de Traefik. Investigar:

1. Webhook GitHub → Dokploy (si Dokploy lo soporta nativamente)
2. GitHub Action que llame a la API de Dokploy post-push
3. Alternativa: script `deploy.sh` que haga `git push` + curl al endpoint de Dokploy

Prioridad alta — cada deploy manual son 3-5 minutos + riesgo de olvidar el reload de Traefik.
