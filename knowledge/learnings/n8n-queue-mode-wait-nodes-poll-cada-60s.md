---
title: n8n queue mode hace que Wait nodes se atasquen ~60s
date: 2026-05-03
source: claude-code-session
tags: [n8n, dokploy, queue, wait]
---

En `EXECUTIONS_MODE=queue`, los nodos Wait con `unit: seconds` parecen atascarse ~60s aunque el valor configurado sea menor (3s, 5s). Causa probable: el worker poll-checa la cola cada 60s por defecto.

## Fix (parcial — verificar)

Añadir al compose Dokploy del worker n8n:

```
QUEUE_RECOVERY_INTERVAL=5
```

No 100% verificado que resuelva del todo. Si vuelve, mirar también:
- `N8N_RUNNERS_ENABLED` (true/false)
- Si el Wait se ejecuta en main process vs worker
- Versión n8n (síntoma visto en 2.x)

Síntoma en UI: ejecución se ve "running" en el Wait, timer real >> el configurado.
