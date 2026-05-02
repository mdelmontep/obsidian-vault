---
title: alpine docker sin bash ni curl — añadir via dockerfile para crons
date: 2026-05-02
source: claude-code-session
tags: [docker, alpine, dokploy, cron]
---

Imágenes `node:*-alpine` no traen `bash` ni `curl` por defecto. Si configuras un schedule en Dokploy que ejecuta `docker exec` con un curl a un endpoint interno, falla:

- `exec: "bash": executable file not found in $PATH` → cambiar Shell Type del schedule a `sh`.
- `sh: curl: not found` → añadir al Dockerfile en la stage runner: `RUN apk add --no-cache curl` (junto al resto de `apk add`).

Aplica también si el cron va a `https://localhost:3000/...`. Llamar a localhost desde el contenedor donde corre la app es lo correcto (evita Cloudflare/Traefik), pero requiere curl instalado.

Diagnóstico: los logs del schedule en Dokploy muestran el error literal del exec. No mirar logs del contenedor — ahí no aparece nada porque el proceso ni siquiera arrancó.
