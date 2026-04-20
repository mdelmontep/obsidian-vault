---
title: dokploy requiere reload manual de traefik tras cada redeploy
date: 2026-04-20
source: claude-code-session
tags: [dokploy, traefik, infra]
---

Cada redeploy de una app en Dokploy deja **Bad Gateway** hasta hacer reload manual de Traefik. No hay auto-reload.

**Ruta**: Dokploy → Settings → Web Server → **Reload**

Ocurrió 3 veces en la misma sesión con FacturaIA. El contenedor arranca correctamente (Next.js escucha en 0.0.0.0:3000, verificable con `netstat -tlnp`), pero Traefik no re-descubre la ruta al contenedor nuevo.

**Diagnóstico rápido**: si Bad Gateway después de redeploy, antes de investigar logs:
1. Verificar que el contenedor está running (Dokploy → app → Docker Terminal → `ps aux`)
2. Hacer reload de Traefik
3. Si sigue sin funcionar, entonces sí mirar logs del build
