---
title: estado y uptime de contenedores de un Dokploy sin SSH, vía su API
date: 2026-07-21
source: claude-code-session
tags: [dokploy, docker, diagnostico, infra]
---
Cuando no tienes acceso SSH al host pero sí la API key de Dokploy, puedes sacar el
estado de los contenedores sin entrar al servidor:

- `curl -H "x-api-key:$K" "$PANEL/api/docker.getContainers"` → contenedores de proyectos
  (name, state, `status` con "Up 3 days (healthy)").
- `.../docker.getContainersByAppNameMatch?appName=<x>` → filtra por substring; con
  `dokploy`/`dokploy-traefik` saca también los de sistema (traefik, dokploy, postgres).

Sirve para descartar "¿se cayó mi servicio?" mirando el uptime ("Up 2 months" = no se
reinició). Para metadata de compose sin fugar secretos usar el wrapper que redacta el
`env` (`dokploy-safe.sh` con `DOKPLOY_API_BASE=$PANEL/api`); el `.one`/`.all` crudos
devuelven todos los secretos en claro.

Gotcha del acceso SSH a estos hosts: el puerto suele ser 5251 (no 22), y el `!` del
prompt corre en TU Mac, no en el host — para tocar el host: sshpass+ssh-copy-id con la
contraseña root de 1Password, o la consola del proveedor. Caso real: diagnóstico del
retraso de 87 min de Meta en Elphis (stack sano, era Meta). Ver [[n8n-status-success-no-implica-camino-critico]].
