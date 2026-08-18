---
title: un docker compose up sin -p levanta un stack GEMELO en vez de recrear el que ya corría
date: 2026-08-18
source: learn-agentesia
tags: [docker, dokploy, incidentes, despliegue, gotcha]
---

**Síntoma.** `cd /opt/aula && docker compose up -d --build web` → aparecen `aula-web-1`, `aula-db-1`, `aula-kong-1`… **junto a** los `aula-womwbl-*` que llevaban 7 días arriba. Dos stacks completos, con las mismas etiquetas de Traefik y bases de datos distintas: el usuario ve una cosa u otra según a quién enrute.

**Causa.** Compose deriva el nombre del proyecto **del directorio** si no le das `-p`. El stack real lo había creado Dokploy con el nombre `aula-womwbl`, desde `/etc/dokploy/compose/aula-womwbl/code/`. Desde otro directorio, el mismo `docker-compose.yml` es *otro* proyecto.

**Comprobar SIEMPRE antes de tocar un compose en un host con Dokploy:**

```sh
docker inspect <contenedor> --format '{{index .Config.Labels "com.docker.compose.project"}}'
docker inspect <contenedor> --format '{{index .Config.Labels "com.docker.compose.project.config_files"}}'
```

Si sale una ruta bajo `/etc/dokploy/compose/`, **ese** es el compose que manda; el que hay en `/opt/<app>/` puede ser solo el origen del que se construyó la imagen.

**El daño colateral que no se ve.** El `--build` reetiquetó `aula-web:latest` a la imagen nueva mientras el contenedor vivo seguía con la vieja **por id**. Estado peor que fallar: nada cambia hoy, pero el siguiente reinicio despliega solo. Al detectarlo, o completas el despliegue o devuelves la etiqueta — dejarlo armado no es una opción.

**Fix.** Construir donde está el `build:`, recrear donde está el stack, y etiquetar la imagen anterior antes de nada:

```sh
docker tag <id-viejo> aula-web:antes-<fecha>          # vuelta atrás
cd /opt/aula && docker compose build web              # solo construye
cd /etc/dokploy/compose/aula-womwbl/code
docker compose -p aula-womwbl up -d --force-recreate --no-deps web
```

Ver [[contenedor-que-no-vuelve-tras-reboot-dos-causas-que-se-confunden]]
