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

## n8n en producción — anti-caídas

n8n se **cuelga sin crashear** — el proceso sigue vivo pero no responde HTTP. `restart: unless-stopped` no sirve para esto porque Docker cree que el contenedor está sano.

**Solución**: healthcheck HTTP que fuerza reinicio:

```yaml
healthcheck:
  test: ["CMD-SHELL", "wget -qO- http://localhost:5678/healthz || exit 1"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 60s
```

**Variables obligatorias de pruning** (sin esto, ejecuciones acumuladas cuelgan n8n):

```yaml
- EXECUTIONS_DATA_PRUNE=true
- EXECUTIONS_DATA_MAX_AGE=168
- EXECUTIONS_DATA_PRUNE_MAX_COUNT=5000
- NODE_OPTIONS=--max-old-space-size=1536
```

**Límite de memoria** para proteger al servidor:

```yaml
deploy:
  resources:
    limits:
      memory: 2G
```

**Versión fija** — nunca `:latest`. Usar tag exacto: `n8nio/n8n:2.15.1`.

Compose de referencia guardado en `~/n8n-agentesia-world-compose.yml`.

## Dokploy — diagnóstico sin SSH

Si SSH al host falla (`ECONNREFUSED 172.18.0.1:22`), diagnosticar desde terminal del contenedor:

```bash
cat /proc/meminfo | head -5          # RAM del host
cat /sys/fs/cgroup/memory.max        # límite contenedor ("max" = sin límite)
env | grep -i "EXECUT\|PRUNE"        # config pruning
ps aux | head -5                     # procesos y CPU time
```

## Generación de credenciales

```bash
# SECRET_KEY_BASE
openssl rand -base64 64 | tr -d '\n'

# Passwords cortos seguros
openssl rand -base64 18 | tr -d '+/=' | head -c 24
```

## Flujo estándar — nuevo compose de cliente

Antes de generar cualquier compose, preguntar siempre en este orden:
1. Dominio (URL del servicio)
2. Email/SMTP — ¿cuenta propia o reutilizar `info@agentesia.madrid`?
3. Servidor — ¿cuál y qué IP?
4. Locale — `es` o `en`
5. `ENABLE_ACCOUNT_SIGNUP` — `false` = solo admin crea usuarios (producción recomendado)
6. Passwords — ¿generar nuevos o reutilizar existentes?

## Puppeteer en Alpine

- `node:20-alpine` no trae Chrome — Puppeteer falla con "Could not find Chrome"
- Solución: `apk add chromium nss freetype harfbuzz ca-certificates ttf-freefont`
- Env vars: `PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser` + `PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true`
- En código: `puppeteer.launch({ executablePath: process.env.PUPPETEER_EXECUTABLE_PATH || undefined })`
- **No hacer fetch HTTP a tu propia API dentro del contenedor** — DNS interno no resuelve el dominio público. Extraer lógica a función compartida e importar directamente.

## Proyectos activos — mapa de infraestructura

| Proyecto | Dominio n8n | Dominio Chatwoot | Servidor |
|---|---|---|---|
| AgentesIA World (Juan) | `n8n.agentesia.world` | `chatwoot.agentesia.world` | `185.99.186.76` |
| AgentesIA Madrid | `n8n.agentesia.madrid` | `chatwoot.agentesia.madrid` | agentesia.madrid |
| Tecnocloud | `n8n.tecnocloud.es` | `chatwoot.tecnocloud.es` | `185.47.13.165` |
| Clinica Zen | `n8nclinicazen.agentesia.madrid` | — | `185.47.13.168` |
| Simarro | `n8nsimarro.agentesia.madrid` | — | `185.47.13.168` |
| FacturaIA | `n8n.agentesia.world` (compartido) | — | `185.99.186.76` |
