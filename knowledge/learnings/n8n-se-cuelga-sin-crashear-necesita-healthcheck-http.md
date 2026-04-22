---
title: n8n se cuelga sin crashear — necesita healthcheck http
date: 2026-04-22
source: claude-code-session
tags: [n8n, docker, dokploy, healthcheck]
---

n8n deja de responder HTTP pero el proceso sigue vivo (PID activo, CPU time acumulado). Docker con `restart: unless-stopped` no lo detecta porque el contenedor no muere.

**Causa principal**: ejecuciones acumuladas sin pruning. La BD crece, las queries se ralentizan, n8n se ahoga.

**Solución**: healthcheck HTTP obligatorio en el compose:

```yaml
healthcheck:
  test: ["CMD-SHELL", "wget -qO- http://localhost:5678/healthz || exit 1"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 60s
```

Combinado con pruning:

```yaml
- EXECUTIONS_DATA_PRUNE=true
- EXECUTIONS_DATA_MAX_AGE=168
- EXECUTIONS_DATA_PRUNE_MAX_COUNT=5000
- NODE_OPTIONS=--max-old-space-size=1536
```

Sin healthcheck, el único síntoma es 502 Bad Gateway en Traefik. El contenedor aparece como "running" en Docker/Dokploy.

Ver también [[dokploy-requiere-reload-manual-traefik-tras-redeploy]]
