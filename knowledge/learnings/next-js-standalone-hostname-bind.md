---
title: next.js standalone bindea a $HOSTNAME, no a 0.0.0.0 (502 tras reverse proxy)
date: 2026-07-05
source: claude-code-session
tags: [nextjs, docker, traefik, dokploy]
---
El server standalone de Next.js (`server.js`) escucha en `process.env.HOSTNAME || "0.0.0.0"`. Docker fija `HOSTNAME=<container_id>`, que resuelve a la IP de la interfaz PRIMARIA (bridge) → Next.js NO escucha en las demás interfaces (p.ej. una overlay `dokploy-network`).

Síntoma: `curl` directo a la IP bridge del contenedor da 200, pero el reverse proxy (Traefik en la overlay) da **502** — el puerto está cerrado en esa IP.

Fix: `HOSTNAME=0.0.0.0` en el env del contenedor web. Verificar el bind con `/proc/net/tcp` dentro del contenedor (`00000000:0BB8` = 0.0.0.0:3000; si sale otra IP, está bindeado a una sola interfaz).

Aplica a cualquier app Next.js standalone detrás de proxy cuando el contenedor está en >1 red.
