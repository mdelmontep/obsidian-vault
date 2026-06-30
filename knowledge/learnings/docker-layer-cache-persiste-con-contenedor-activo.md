---
title: docker layer cache persiste si hay contenedor activo referenciando la capa
date: 2026-06-30
source: claude-code-session
tags: [docker, dokploy, infra, cache]
---

`docker builder prune -f` (o `-af`) no purga capas referenciadas por un contenedor en ejecución. El build siguiente consume la caché aunque el código haya cambiado.

**Síntoma**: tras `prune`, el contenedor arranca con código viejo. `docker exec <ctr> cat <archivo>` muestra versión anterior.

**Fix**: desde el directorio del compose en Dokploy:
```
docker compose build --no-cache <service>
docker compose up -d <service>
```
Ruta típica: `/etc/dokploy/compose/<stack>/code/`

**Alternativa segura**: parar el contenedor primero (`docker compose stop <svc>`), luego `builder prune -af`, luego build+up.

Relacionado: [[docker-compose-env-not-recreate]]
