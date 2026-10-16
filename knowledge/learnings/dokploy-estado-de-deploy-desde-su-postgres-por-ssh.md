---
title: el estado de un deploy de dokploy se lee de su postgres por ssh, sin api ni login
date: 2026-10-16
source: agency-portal (verificación del deploy de #853)
tags: [dokploy, deploy, verificacion]
---
Cuándo: hay que confirmar que un merge quedó desplegado y la API no sirve (sin API key válida, el login por sesión lo deniega un hook, o `application.one` volcaría el env). Es la vía inversa de [[dokploy-api-docker-getcontainers-estado-sin-ssh]].

Patrón: en el host de Dokploy, `docker exec <dokploy-postgres.1.…> psql -U dokploy -d dokploy -At`, tabla `deployment`. Las columnas van en camelCase, así que hay que entrecomillarlas: `title`, `status`, `"createdAt"`, `"finishedAt"`, `"applicationId"` (o `"composeId"`). Ordenar por `"createdAt" desc`: la API las devuelve sin orden ([[dokploy-api-deployments-sin-ordenar]]).

- `title` es el mensaje del commit entero, de varias líneas: cortarlo con `left(title,40)`.
- Es solo lectura y no toca secretos: la tabla no guarda el env.
- Portal: host `root@10.250.0.166:5251` por la VPN, applicationId `oszJEikiQjiLc7Jp4Tv0z`.
