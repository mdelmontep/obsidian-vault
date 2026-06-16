---
title: docker e infraestructura — reglas y patrones
date: 2026-04-20
source: claude-md-migration
tags: [docker, traefik, dokploy, infra]
---

# Docker / Infraestructura

## Healthchecks en Alpine — `curl` no `wget`

- `node:*-alpine` con `apk add curl` **no tiene `wget`**. Usar siempre `curl` en el test del healthcheck.
- Correcto: `test: ["CMD", "curl", "-sf", "http://localhost:3000/api/health"]`
- Incorrecto: `test: ["CMD", "wget", "-qO-", "..."]` → healthcheck falla silenciosamente, Docker nunca marca el contenedor healthy.

## `depends_on: condition: service_healthy` solo para dependencias bloqueantes

- Si el servicio tiene fallback (Redis → in-memory, BD externa → degraded), usar `depends_on: [redis]` sin condición.
- Con `condition: service_healthy`, si Redis no levanta el app tampoco arranca → degraded se convierte en outage total.
- Regla: `condition: service_healthy` solo cuando el servicio es literalmente imprescindible para que la app funcione (Postgres para n8n, sí. Redis para rate-limit con fallback, no).

## Cloudflare DNS proxiado bloquea Let's Encrypt

- Si el A record de un dominio tiene la nube naranja en Cloudflare (proxied), el ACME HTTP-01 challenge recibe `204` de Cloudflare en lugar del token → cert nunca emite.
- Traefik logs: `invalid authorization: 403 ... Invalid response from http://dominio/.well-known/acme-challenge/...: 204`
- Solución: poner el A record en **DNS only** (nube gris) ANTES de configurar Let's Encrypt. Una vez emitido el cert, se puede volver a proxiar si se quiere.
- Caso real TuFacturaIA 2026-05-13: `tufacturaia.com` con DNS proxiado → cert bloqueado. Fix pendiente Dani.

## GitHub App Dokploy — requiere owner de la org

- La GitHub App de Dokploy debe crearse logueado con una cuenta que sea **owner** de la organización GitHub donde está el repo.
- Si se crea con una cuenta personal sin ese rol, la org no aparece en la lista de instalación ("Install App").
- Workaround si no tienes owner: usar Git + SSH deploy key en lugar de GitHub App (Dokploy → Git → `git@github.com:org/repo.git` → Add SSH Key → añadir public key en GitHub repo Settings → Deploy keys).
- Caso real TuFacturaIA 2026-05-13: repo en `AgentesIA-MAdrid`, app creada con `mdelmontep` (no owner) → org no aparecía. Fix: crear app logueado como `AgentesIAMadrid` (owner de la org).

## `NEXT_PUBLIC_*` vars en Dokploy requieren prefijo exacto

- Son build args en docker-compose, no solo runtime envs. Sin el prefijo `NEXT_PUBLIC_` se inyectan como env runtime pero el bundle del browser las recibe vacías.
- En Dokploy Environment Settings, la clave debe ser exactamente `NEXT_PUBLIC_SUPABASE_URL`, no `SUPABASE_URL`.
- Síntoma: `env | grep SUPABASE` en el contenedor muestra `NEXT_PUBLIC_SUPABASE_URL=` (vacío) aunque en Dokploy UI esté con valor → el compose referencia `${NEXT_PUBLIC_SUPABASE_URL}` pero la UI tenía `SUPABASE_URL`.

## Dokploy — Compose vs UI Variables

- Variables de la UI de Dokploy solo llegan al contenedor si el compose las referencia con `${VAR}`
- **Secrets** (API keys, passwords) → UI de Dokploy + `${VAR}` en el compose
- **Config estructural** (flags, URLs fijas, puertos) → hardcodeada en el compose
- Si `env | grep VAR` en el contenedor devuelve vacío aunque esté en la UI → falta el `${VAR}` en el compose

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

Ocurrió 3 veces seguidas con TuFacturaIA. No hay auto-reload. Pendiente investigar webhook GitHub → Dokploy para deploy automático.

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
- **Alpine sin bash/curl** — `node:*-alpine` no trae ninguno. Para crons Dokploy via `docker exec`: Shell Type `sh` + `apk add --no-cache curl` en Dockerfile. Ver [[alpine-docker-sin-bash-ni-curl-anadir-via-dockerfile-para-crons]]

## Dokploy — schedules (crons) vía API

- Los crons de un stack se pueden **crear/listar por API**, no solo desde el panel. Auth header `x-api-key` (token en 1Password `Dokploy API · <host>`).
- `GET /api/schedule.list?id=<composeId|applicationId>&scheduleType=compose|application` — lista (copia el patrón de un cron existente antes de crear).
- `POST /api/schedule.create {name, cronExpression, command, scheduleType, composeId|applicationId, serviceName, shellType, script:"", enabled}`.
- `POST /api/schedule.runManually {scheduleId}` — ejecuta ya; el classifier lo bloquea (mutación prod) → lanzar con `!` o desde la UI app.
- `composeId`/`applicationId` salen de `GET /api/project.one?projectId=…` (en versiones nuevas apps/compose anidan bajo `environments[]`).
- Ojo: el panel `/admin/system` de la app (tabla `cron_runs`) y los "Deployments" del schedule en Dokploy miden cosas distintas — la app registra cualquier ejecución del endpoint; Dokploy solo las que dispara su scheduler.

## Dokploy AgentesIA — acceso SSH

| Host | IP | Puerto SSH | Uso |
|---|---|---|---|
| Dokploy viejo | `185.47.13.166` | `5251` | n8n compartido, AgentesIA, Tecnocloud, Simarro |
| Dokploy nuevo TuFacturaIA | `185.47.13.170` | `5251` | `app.tufacturaia.com`, `n8n.tufacturaia.com` (desde 2026-05-13) |

- **Usuario**: `root` · **Key**: `~/.ssh/id_ed25519` (mismo en ambos)
- Comando: `ssh -p 5251 root@<IP>`
- Para autorizar la key: `ssh-copy-id -i ~/.ssh/id_ed25519.pub -p 5251 root@<IP>`
- Si puerto 22 da `Connection refused` → es porque SSH escucha en `5251`. NO port-scan (bloqueado por Claude classifier + ruidoso).

## Proyectos activos — mapa de infraestructura

| Proyecto | Dominio n8n | Dominio Chatwoot | Servidor |
|---|---|---|---|
| AgentesIA World (Juan) | `n8n.agentesia.world` | `chatwoot.agentesia.world` | `185.99.186.76` |
| AgentesIA Madrid | `n8n.agentesia.madrid` | `chatwoot.agentesia.madrid` | agentesia.madrid |
| Tecnocloud | `n8n.tecnocloud.es` | `chatwoot.tecnocloud.es` | `185.47.13.165` |
| Clinica Zen | `n8nclinicazen.agentesia.madrid` | — | `185.47.13.168` |
| Simarro | `n8nsimarro.agentesia.madrid` | — | `185.47.13.168` |
| TuFacturaIA (actual) | `n8n.agentesia.world` (compartido) | — | `185.99.186.76` |
| TuFacturaIA-prod nuevo | (n8n se queda en `agentesia.world`) | — | `185.47.13.170` (VPS dedicado, Dokploy nuevo creado 2026-05-12, vacío al inicio) |
