---
title: dokploy requiere reload manual de traefik tras cada redeploy
date: 2026-04-20
source: claude-code-session
tags: [dokploy, traefik, infra]
---

Cada redeploy de una app en Dokploy deja **Bad Gateway** hasta hacer reload manual de Traefik. No hay auto-reload.

**Ruta**: Dokploy → Settings → Web Server → **Reload**

Ocurrió 3 veces en la misma sesión con TuFacturaIA. El contenedor arranca correctamente (Next.js escucha en 0.0.0.0:3000, verificable con `netstat -tlnp`), pero Traefik no re-descubre la ruta al contenedor nuevo.

**Diagnóstico rápido**: si Bad Gateway después de redeploy, antes de investigar logs:
1. Verificar que el contenedor está running (Dokploy → app → Docker Terminal → `ps aux`)
2. Hacer reload de Traefik
3. Si sigue sin funcionar, entonces sí mirar logs del build

**Mismo fallo con cert Let's Encrypt en servicio/dominio NUEVO** (2026-06-18, MCP server): tras `domain.create`+`compose.deploy`, el router enruta (http→https OK, `/health` 200 por https-insecure) pero **el cert LE no se emite** — Traefik sirve su cert default y **crt.sh sale vacío** — aunque el dominio marque `DNS Valid` y el entrypoint `websecure` ya traiga `certResolver: letsencrypt` por defecto. Causa: **Traefik no recargó** y no intentó la emisión. Fix: reload. Señal inequívoca = cert default + 0 entradas CT tras varios redeploys → es falta de reload, NO config ni rate-limit de LE (no pierdas 1h diagnosticando ACME).

**Endpoint API** (reload sin panel, va por 443): `POST https://<dokploy>/api/settings.reloadTraefik` con `x-api-key` → `200 true`. Los `settings.reloadServer`/502 transitorios posteriores son el propio Traefik reiniciándose; el cert emite en <1 min.
