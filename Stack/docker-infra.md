---
title: docker e infraestructura — reglas y patrones
date: 2026-04-20
source: claude-md-migration
tags: [docker, traefik, dokploy, infra]
---

# Docker / Infraestructura

## Reglas Traefik en Dokploy

- **Solo el contenedor que Traefik enruta va en `dokploy-network`**. El resto de servicios usan red interna propia.
- Declarar siempre `chatwoot-internal` (o equivalente) como red bridge para comunicación inter-servicios
- Labels de Traefik siempre con nombres únicos por stack para evitar conflictos
- **Naming de routers**: patrón `<servicio>-<cliente>` — ej: `chatwoot-agentesia`, `chatwoot-tecnocloud`, `n8n-tecnocloud`. Evita conflictos cuando el mismo servicio corre en múltiples clientes en el mismo host

```yaml
# Patrón correcto — solo el contenedor principal en dokploy-network
networks:
  dokploy-network:
    external: true
  <stack>-internal:
    driver: bridge
```

- Sin label `traefik.docker.network` → Traefik no enruta aunque el contenedor esté en la red
- Si un stack satura `dokploy-network` → síntoma: otros servicios dan bad gateway al activarlo

## Healthchecks

- Postgres: usar `pg_isready -U postgres -d <db>` **hardcodeado**, no con `${VAR}` — no se expande en CMD-SHELL
- `retries: 10` + `start_period: 30s` para Postgres en primer arranque
- Redis: `redis-cli ping` es suficiente

## Passwords y variables

- **Sin caracteres especiales** (`$`, `#`, `&`, `@`) en passwords de Redis y Postgres — se corrompen en Docker Compose
- Si Postgres o Redis ya arrancaron con password corrupta, el volumen persiste — hay que borrarlo antes de redesplegar
- SMTP: hardcodear valores directamente en el compose si las `${VAR}` no se inyectan correctamente desde Dokploy

## Traefik reload obligatorio tras redeploy

Cada redeploy en Dokploy deja **Bad Gateway** hasta hacer reload manual de Traefik. El contenedor arranca correctamente (Next.js escucha en 0.0.0.0:3000, verificable con `netstat -tlnp`), pero Traefik no re-descubre la ruta.

**Ruta**: Dokploy → Settings → Web Server → **Reload**

Diagnóstico rápido si Bad Gateway post-redeploy:
1. Verificar contenedor running (`ps aux` en Docker Terminal de Dokploy)
2. Hacer reload de Traefik
3. Si sigue, entonces mirar logs del build

Ocurrió 3 veces seguidas con FacturaIA. No hay auto-reload. Pendiente investigar webhook GitHub → Dokploy para deploy automático.

## Generación de credenciales

```bash
# SECRET_KEY_BASE
openssl rand -base64 64 | tr -d '\n'

# Passwords cortos seguros
openssl rand -base64 18 | tr -d '+/=' | head -c 24
```
