---
title: supabase con egress restringido tumba la app entera vía healthcheck → Traefik 404 (docker "healthy" engaña)
date: 2026-07-10
source: claude-code-session
tags: [supabase, dokploy, traefik, incidente, healthcheck]
---
Si un proyecto Supabase supera su cuota de **egress** (o cualquier "restricted"),
devuelve en CADA llamada: `Service for this project is restricted ... exceed_egress_quota`.
Cascada en una app desplegada (Dokploy/Traefik): el healthcheck HTTP de la ruta toca
Supabase → falla → el LB marca el backend sin instancias sanas → Traefik responde su
`404 page not found` en `text/plain` (NO el 404 de la app, que sería HTML).

Engaño clave: `docker ps` muestra el contenedor `(healthy)` — ese es el healthcheck
del CONTENEDOR, distinto del de la RUTA de Traefik. No es OOM ni crash.

Diagnóstico: `curl -I` da 404 `text/plain` + `docker logs` llenos de la misma línea
de Supabase. Fix: restaurar el proyecto (subir plan / quitar spend cap). La cuota de
egress es por ciclo mensual y se resetea; en Free (~5GB) recurre → prod real va a Pro.
Al restaurar, el healthcheck pasa y Traefik re-registra la ruta SOLO, sin deploy ni
recarga. Ver [[dokploy-requiere-reload-manual-traefik-tras-redeploy]].
