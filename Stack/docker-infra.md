---
title: docker e infraestructura — reglas y patrones
date: 2026-04-20
source: claude-md-migration
tags: [docker, traefik, dokploy, infra]
---

# Docker / Infraestructura

## El `env` está CIFRADO en la base de Dokploy — la receta de leer-fusionar-escribir no vale

- `application.update` reemplaza el bloque entero, pero **no hay forma de leerlo**: la API lo devuelve en
  claro y el wrapper lo borra; su propia base lo guarda cifrado (460 caracteres sin un `=`).
- Sustituto probado (7-ago): reconstruir el bloque desde la fuente local, y **antes de escribir** comparar
  la huella SHA-256 de cada variable ya presente en el contenedor (`docker exec … printenv`, por SSH)
  contra la tuya. Coinciden → reconstruir no pierde nada. Ver
  [[dokploy-guarda-el-env-cifrado-la-receta-de-leer-fusionar-escribir-no-vale]].
- El guion corre EN EL HOST y sólo imprime nombres, longitudes y huellas: ningún valor cruza a la sesión.
- Verificar siempre en el plano de datos, no en el de control. Y el contenedor no lo toma al vuelo.

## El `env` está CIFRADO en la base de Dokploy — la receta de leer-fusionar-escribir no vale

- `application.update` reemplaza el bloque entero, pero **no hay forma de leerlo**: la API lo devuelve en
  claro y el wrapper lo borra; su propia base lo guarda cifrado (460 caracteres sin un `=`).
- Sustituto probado (7-ago): reconstruir el bloque desde la fuente local y, **antes de escribir**, comparar
  la huella SHA-256 de cada variable ya presente en el contenedor (`docker exec … printenv`, por SSH)
  contra la tuya. Coinciden → reconstruir no pierde nada. Ver
  [[dokploy-guarda-el-env-cifrado-la-receta-de-leer-fusionar-escribir-no-vale]].
- El guion corre EN EL HOST y sólo imprime nombres, longitudes y huellas: ningún valor cruza a la sesión.
- Verificar en el plano de datos, no en el de control. Y el contenedor no lo toma al vuelo.

## API Dokploy: `compose.one` y `schedule.one` devuelven el `env` COMPLETO

- Ambos endpoints incluyen el bloque `env` entero del compose (todos los secrets: DB, API keys de terceros, tokens) en la respuesta, aunque solo se pida para leer metadata (autoDeploy, appName, último deploy).
- Nunca llamarlos solo para comprobar config — usar `deployment.allByCompose`/`deployment.one` (no incluyen env) o pedirlo al usuario vía panel.
- Fuga real 2026-07-03 (TuFacturaIA): se volcó a un chat de Claude Code el env completo de prod (service role key, API keys LLM, tokens WhatsApp, claves de cifrado) al llamar `compose.one` para revisar si un deploy había terminado.

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

## Identidad del build: qué commit hay sirviendo (no ponerlo a mano en el panel)

- Un `NEXT_PUBLIC_APP_VERSION` escrito como literal en el env del panel **se congela en el primer build y miente en todos los deploys siguientes** — peor que no tenerlo, porque invita a confiar en él. `NEXT_PUBLIC_*` se hornea en tiempo de compilación.
- Que lo calcule el build: `APP_VERSION` como build arg si el orquestador puede inyectar el commit (Dokploy hoy no lo pasa), y si no, marca de tiempo generada en `next.config.ts` y expuesta vía `env:`. No sirve leer el SHA dentro de la imagen: `.git` suele estar fuera del contexto por `.dockerignore`.
- Verificar que queda **inlined** (`grep` del valor en `.next/server/app/api/health/route.js`), no recalculado al arrancar el contenedor: ahí está la diferencia entre un dato útil y uno inútil.
- Para qué sirve: al dudar de un despliegue, contrastar `curl /api/health` contra el `finishedAt` del deployment. Sin esto (caso real 27-jul) se gastaron **tres escrituras contra la BD de prod** para averiguar si el contenedor era el nuevo. Ver [[cambiar-la-semantica-de-una-columna-el-compositor-no-es-el-punto-de-persistencia]].
- Metadata de deployments sin volcar secretos: `dokploy-safe.sh "/api/compose.one?composeId=<id>"` → `deployments[]` trae `description: Commit: <sha>`, `status` y `finishedAt`, y `autoDeploy`.
- **Si no hay marca de compilación que aprovechar, sella el CONTENIDO**: `RUN` en el `Dockerfile` (después del `COPY`, antes del `CMD`) que hashea lo que acaba de entrar en la imagen, servido por un endpoint. Se compara con el digest calculado en local sobre un árbol limpio. Es la única vía que **no depende del SSH** — y el SSH se cae. Ver [[sellar-la-imagen-en-el-build-para-saber-que-corre-en-prod-sin-shell]].
- ⚠️ **Que Dokploy no pase el commit al build no es un detalle a rodear con una env var del panel**: su env es de *runtime* y **sobrevive a la imagen**, así que una imagen vieja cantaría el SHA nuevo que alguien tecleó. Las peticiones para que lo inyecte llevan abiertas desde 2025 (Dokploy#2715, #4006).
- La lista de **qué** sellar se **deriva del `.dockerignore`**, nunca se escribe a mano: una lista paralela nace divergida el mismo día. Y sus patrones van **anclados a la raíz** — `node_modules` no tapa `sub/node_modules`.

## `NEXT_PUBLIC_*` vars en Dokploy requieren prefijo exacto

- Son build args en docker-compose, no solo runtime envs. Sin el prefijo `NEXT_PUBLIC_` se inyectan como env runtime pero el bundle del browser las recibe vacías.
- En Dokploy Environment Settings, la clave debe ser exactamente `NEXT_PUBLIC_SUPABASE_URL`, no `SUPABASE_URL`.
- Síntoma: `env | grep SUPABASE` en el contenedor muestra `NEXT_PUBLIC_SUPABASE_URL=` (vacío) aunque en Dokploy UI esté con valor → el compose referencia `${NEXT_PUBLIC_SUPABASE_URL}` pero la UI tenía `SUPABASE_URL`.

## Un servicio AUSENTE se levanta solo, sin el Deploy entero

Si a un stack de Dokploy le falta **un** contenedor pero el servicio **sigue declarado** en el compose,
no hace falta Deploy (que reinicia todos los sanos y es prod):

```
cd /etc/dokploy/compose/<stack>/code && docker compose up -d <servicio>
```

- Los demás salen listados como `Running` y **no se reinician**; verificado con `Up 6 weeks` intactos.
- **El compose no se edita**, así que el panel NO queda desincronizado — lo que la disciplina prohíbe
  es editar en disco (el Deploy lo regenera), no arrancar algo ya declarado.
- Antes: comprobar que el servicio está en el compose (`grep -nE "^  [a-z-]+:"`) y que **sus volúmenes
  existen** (`docker volume ls`) — si el volumen sobrevive, no se ha perdido nada.
- Verificar por el **fallo exacto**, no por `/health`: `docker exec <consumidor> wget -qO- http://<servicio>:<puerto>/ping`.
- ⚠️ No dar por hecho lo que diga tu máquina del subcomando: en el Mac con Colima `docker compose` **no
  existe**, y en el host de AGH es v5.2.0. Caso real (17-ago): ClickHouse de Langfuse ausente 10 días,
  reparado en 20 s por esta vía tras un día dado por bloqueado en «hay que hacer Deploy».

## Dokploy — alta de un servicio Compose por API (sin panel)

- Secuencia probada (marketing-runner, 13-ago): `compose.create` `{name, environmentId, composeType:'docker-compose'}` → `compose.update` `{composeId, sourceType:'github', owner, repository, branch, composePath, githubId, autoDeploy}`. El `environmentId` y el `githubId` se copian de un servicio hermano vía `dokploy-safe.sh /api/project.one` y `/api/compose.one`.
- El `env` del servicio es UN campo de reemplazo completo. Escribirlo por API solo es seguro en un servicio NUEVO (no hay nada que pisar); en uno existente no se puede ni leer con seguridad (el guard anti-fuga redacta) → panel a mano.
- Secretos al env por API sin imprimirlos: construir el JSON en un heredoc de python con los valores de `opsa read` como argv, y `curl -d @-`.
- Deploy: `compose.deploy` `{composeId}` y sondear `composeStatus` (`idle → running → done|error`) por `compose.one` (siempre vía dokploy-safe).

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

## Runtime local en esta Mac (colima, no Docker Desktop)

- El runtime es **colima** (`colima start`), NO Docker Desktop → `open -a Docker` falla ("Unable to find application"). Arrancar con `colima start` (levanta una VM ~15s).
- **No hay plugin `docker compose`** → `docker compose up -d` da "unknown shorthand flag: 'd'". Levantar servicios con `docker run` directo. Dev local AGH: `docker run -d --name agh-pg -e POSTGRES_USER=user -e POSTGRES_PASSWORD=pass -e POSTGRES_DB=agh_dev -p 5433:5432 pgvector/pgvector:pg16` + `docker run -d --name agh-redis -p 6380:6379 redis:7-alpine redis-server --appendonly yes --maxmemory-policy noeviction`.
- Scripts que asumen `docker compose exec` (p.ej. `db:check-drift` de AGH) fallan → replicar con `docker exec <container>`.
- **El proceso `com.apple.Virtualization.VirtualMachine` que come CPU/RAM ES la VM de colima** (Lima sobre Virtualization.framework). Identificarlo con `lsof -p <pid> | grep colima` → `~/.colima/_lima/colima/disk`. Reserva de golpe los GiB configurados (`colima list`) y **no los devuelve** aunque dentro solo se usen 700 MB; con la VM ociosa cuesta además ~1/3 de core de overhead del hipervisor. Llevaba 3 días encendida con 8 GiB tomados (03-ago).
- **Auto-apagado instalado (03-ago)**: `~/.local/bin/colima-idle-stop.sh` + LaunchAgent `madrid.agentesia.colima-idle-stop` (cada 300 s) paran la VM tras ~30 min sin uso; `~/.local/bin/docker` es un wrapper que la vuelve a levantar (~1 min) y delega en `/opt/homebrew/bin/docker`. Log: `~/.colima/idle-stop.log`; depurar con `COLIMA_IDLE_DEBUG=1`. Por qué las señales son esas → [[presencia-y-cpu-no-miden-uso-el-healthcheck-falsea-la-senal]]
- **Tras parar la VM, un contenedor con `restart=no` NO vuelve** (se pierde el de test, bien; se pierde también tu postgres de dev, mal). Los permanentes a `docker update --restart unless-stopped <c>`. Y si añades un servicio permanente nuevo, mételo en `PERSISTENT` del script o sus healthchecks contarán como uso y la VM no se apagará nunca.
- **`docker events --until 30s` significa "hasta hace 30 s", no "durante 30 s"** → ventana invertida y 0 eventos, que se lee como "no pasa nada". Para mirar hacia atrás: `--since 6m --until 0s`. Para muestrear hacia adelante: lanzarlo en background y matarlo tras N segundos.
- ⚠️ **`docker info` → error NO significa "daemon parado"**: con colima corriendo (`colima status` → `Running`) puede ser solo el **contexto** — `export DOCKER_HOST="unix://$HOME/.colima/default/docker.sock"` y funciona. Un agente lo leyó como límite del entorno y estuvo a punto de dejar sin construir la imagen de una PR que tocaba el arranque de prod (14-ago). Un «no se puede medir» merece un intento propio antes de aceptarse.

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

## Dokploy — acceso SSH al host y contraseña root de tanda

- Puerto SSH de estos hosts: **5251** (el 22 está cerrado). Tanda `185.47.13.x`: Clínica Zen `.168`, Simarro `.169`, tufacturaia `.170`, Elphis `.173`. Además el Dokploy de Tecnocloud `dokploymanu` = `185.99.186.76` (host DOKPLOYMANU, corre TuCRMIA).
- **Todos los Dokploy de Manu comparten la contraseña root** — la del item `Dokploy SSH root — Clínica Zen` (vault Clinica Zen) abre TODOS, incluso el de Tecnocloud en otro proveedor (`185.99.186.x`). Si "falta la clave SSH de un host", no resetees: usa esa. Ojo: la de "SSH Laserys" y la "plantilla" NO valen.
- Los 4 hosts tienen ya en su vault: documento `SSH root — <host> (ed25519, compartida)` (clave privada) + ítem SERVER `Dokploy SSH root — <host>`. Alias local `ssh <host>` en `~/.ssh/config`.
- Autorizar clave nueva: `sshpass -e ssh -p 5251 root@<IP>` con `SSHPASS` leído por `opsa` (nunca `ssh-copy-id` sin sshpass → prompt interactivo). El clasificador de Claude Code bloquea ese SSH → correrlo con `!`. Ver [[vps-dokploy-de-una-tanda-comparten-password-root]].

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
- `POST /api/schedule.runManually {scheduleId}` — ejecuta ya (devuelve `true`). El classifier bloquea estas mutaciones de forma irregular: el 28-jul dejó pasar `runManually` y frenó dos veces un `schedule.create` idéntico a otro que sí había pasado → si te corta, lánzalo con `!` o desde la UI.
- **`schedule.list` usa query params planos, NO el `input=<json>` de tRPC** (`?id=…&scheduleType=…`); si te devuelve "Input validation failed", el `zodError` de la respuesta te dice los campos exactos que espera. Y **vuelca el `env` igual que `.one`/`.all`** porque cada fila trae el `compose` embebido → siempre vía `dokploy-safe.sh` (el hook global ya lo bloquea en crudo desde el 28-jul).
- **Cada schedule tiene su propio `timezone`**: `NULL` = **UTC**, o `Europe/Madrid` explícito, y conviven los dos en el mismo stack (en TuFacturaIA, 13 en Madrid y 31 en UTC). Consecuencia: **no deduzcas la expresión cron de las horas de `cron_runs`** sin mirar antes la zona de ESE schedule — una "corrección" así dejó `mcp-dcr-cleanup` documentado como diario cuando era semanal. Ver [[estar-en-el-catalogo-de-crons-no-es-estar-programado]]
- Verificar un cron nuevo = `runManually` + comprobar la fila en `cron_runs`, no el `done` de Dokploy: ese solo dice que el shell salió con 0. Vale como señal únicamente si el comando propaga el HTTP (`sign-call.sh` sí: falla con ≥400 y con `000`).
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
| AGH Ibérica (agente "Carlos") | — | — | `185.99.186.138` (Dokploy dedicado; panel `agh.agentesialabs.com`, SSH `-p 5251`) |

## Dokploy: desplegar un stack Compose por API + exponerlo por Traefik

- **En Dokploy, 200 y releer NO significan aplicado.** La API escribe en su BD, no en el disco: `certificates.update` guardó la cadena TLS completa, la relectura la confirmaba y Traefik siguió sirviendo la vieja **horas**. Lo materializa `settings.reloadTraefik`/`reloadServer` (segundos de 502 en el host). Y `application.saveEnvironment` responde 200 y **no guarda nada** — el bueno es `application.update`, que además reemplaza el bloque entero (leer, fusionar, escribir). Verificar SIEMPRE en el plano de datos: `openssl s_client`, `docker exec <c> env`, una llamada que devuelva el efecto. Ver [[dokploy-guarda-en-su-bd-y-no-toca-el-disco]]
- **Nombres de endpoint no adivinables**: `certificates.all` (plural) existe, `certificate.all` da 404. Tantear con `POST {}`: 400 = existe y valida entrada, 404 = no existe. Y `certificates.update` acepta **actualización parcial** (solo exige `certificateId`), así que se puede corregir un certificado sin que la clave privada viaje.
- **Deploy por API** (`DOKPLOY_API_KEY`, header `x-api-key`, base `https://<panel>/api`, estilo tRPC `/api/<procedure>`): `compose.create` (**`composeType: docker-compose`**, NO `stack`/swarm — con swarm se ignoran `mem_limit`, `depends_on: condition:service_healthy` y `configs`) → `compose.update` (`sourceType: raw`, `composeFile`, `env`) → `domain.create` (`domainType: compose`, `serviceName`, `port`, `https`, `certificateType: letsencrypt`) → `compose.deploy`. `application.saveEnvironment` exige además `buildArgs`.
- **Enrutado**: el docker-provider de Traefik vigila `dokploy-network` (`exposedByDefault:false`). Dokploy inyecta los labels al añadir el Domain → el servicio debe estar EN `dokploy-network` y **escuchar en 0.0.0.0** (ver [[next-js-standalone-hostname-bind]]). NO publicar `ports:` al host (choca con puertos en uso / expone servicios internos).
- **Compose service conectado a git ≠ compose pegado en el panel**: si el servicio tiene Provider = GitHub (repo+branch, Autodeploy), Dokploy usa el `docker-compose.yml` DEL REPO en cada push, así que un cambio de `build.context`/`dockerfile` commiteado ya vale y NO hay que tocar el panel (verificado 25-jul en `feedback-runner` de agency-portal: el log del deploy mostraba las rutas COPY nuevas). Solo los servicios con `sourceType: raw` llevan el YAML dentro de la BD de Dokploy. Míralo en la pestaña General → Provider antes de planear "actualizar el panel".
- **Editar por SSH = efímero**: Dokploy regenera el compose/env desde su BD (SQLite) al pulsar Deploy → editar SIEMPRE en el panel/API. Un `docker compose up` a mano en `/opt/...` funciona pero queda FUERA del panel (invisible para el equipo) — solo emergencia.
- Aislar un stack pesado (Langfuse/ClickHouse) del resto: `mem_limit` por servicio + rotación de logs (`logging: max-size/max-file`) — protege a los demás containers del box. Ver [[langfuse-v3-selfhost-deploy-gotchas]].
- **Colima solo comparte `$HOME`**: un bind mount desde `/tmp` no falla, crea un DIRECTORIO vacío y el error sale luego como `MODULE_NOT_FOUND`. Comprobar con `ls -la` dentro del contenedor. Incluye receta de instalación y el OOM de `next build` por heap topado a 2 GB. Ver [[colima-solo-monta-home-el-bind-mount-de-tmp-crea-un-directorio]]
- **Nadie vigila el EOL del runtime: Dependabot mira CVEs, no fechas** — 88 días con Node EOL en prod sin un aviso, y el bump propuesto llevaba a un tag congelado. Check mensual contra endoflife.date, alojado FUERA de la infra que puede caerse. Ver [[dependabot-no-avisa-de-eol-de-runtime]]

- **Detrás de Traefik, `request.url` de un route handler trae el host INTERNO del contenedor**: un redirect
  construido con su `origin` sale como `Location: http://0.0.0.0:3000/…`. En local es invisible porque los
  dos hosts coinciden. Usar `Location` **relativo**, nunca `X-Forwarded-Host` (la escribe quien esté
  delante). Ver [[request-url-detras-de-un-proxy-trae-el-host-interno-del-contenedor]]

## Operar un stack: las dos que no estaban escritas (movidas del CLAUDE.md global, 4-ago-2026)

Vinieron del `CLAUDE.md` global al podarlo. La tercera de aquella terna —«200 + releer OK ≠ aplicado»—
**ya estaba** aquí y mejor contada (§ del `reloadTraefik`), así que no se duplica.

- **El compose y el env de un stack se editan EN EL PANEL** + Save + Deploy. Editar el fichero en el
  disco por SSH es temporal: Dokploy lo **regenera desde su BD** y el cambio desaparece sin avisar.
- **El env de un orquestador son 3 capas y hay que verificar las tres**: (1) el manifest/panel,
  (2) el container **RECREADO** —no `restart`, que conserva el env viejo— y (3) `docker exec <c> env`,
  que es la única que dice qué ve el proceso.

## Movido desde `hot.md` (poda del 14-ago)

Estaban en el índice de arranque, que se paga en TODA sesión sin disparador claro, y la regla del propio `hot.md` dice que un gotcha de un stack concreto no entra ahí: su casa es este fichero, que ya se carga cuando tocas lo suyo.

- **`curl` en macOS valida una cadena TLS que GitHub y Node rechazan** — completa el intermedio por su cuenta y te engaña; cuenta posiciones con `openssl s_client`. Ver [[cadena-tls-incompleta-curl-en-macos-la-salva-y-engana]]
