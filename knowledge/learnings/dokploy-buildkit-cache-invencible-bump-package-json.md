---
title: Dokploy BuildKit cachea COPY aunque cambien archivos → bump package.json
date: 2026-05-16
source: claude-code-session
tags: [dokploy, docker, buildkit, deploy, gotcha]
---

En Dokploy con BuildKit, la layer `COPY . .` puede salir CACHED aunque `src/` haya cambiado y el `transferring context` muestre el tamaño nuevo. Síntomas:

- Cambias código, pushas, deploy "Done", URL devuelve la versión vieja.
- Imagen hash distinto pero todos los `#N CACHED`.
- Container queda `Running` (no `Recreated`).

**Cosas que NO bastan**:
- Añadir/modificar `.deploy-marker` (BuildKit a veces ignora archivos pequeños o sin cambio aparente).
- `ARG CACHEBUST` con valor estático en Dockerfile.
- Botón "Reload" de Dokploy (solo reinicia container con la imagen existente).

**Lo que SÍ funciona**: bump `package.json.version` (0.1.0 → 0.1.1). El layer `COPY package.json package-lock.json* ./` está antes que `COPY . .` y al cambiar invalida toda la cadena posterior incluyendo `RUN npm run build`.

Alternativa nuclear: SSH al host, `docker builder prune -af` o `docker compose build --no-cache`.
