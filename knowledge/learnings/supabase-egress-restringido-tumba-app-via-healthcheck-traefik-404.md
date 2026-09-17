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

**Mismo 404, causa mucho más tonta** (17-sep, ecobox): el host no estaba dado de alta en
*Domains*. Para Traefik `www.x.es` y `x.es` son hosts distintos y no heredan nada: sin su
entrada no hay router, así que contesta ese `404 page not found` en `text/plain` y **tampoco
le pide certificado a Let's Encrypt** — el aviso de certificado y el 404 son el mismo fallo,
no dos. Fix: añadir el dominio en Domains (mismo Path/Port que el que ya sirve).

Discriminar entre las tres causas es barato y hay que hacerlo ANTES de tocar nada: `curl` al
**host exacto** que abre el usuario, dos veces. Persistente en un host y 200 en otro → falta
el alta. Transitorio en todos → era la ventana del redeploy (Dokploy baja el viejo antes de
levantar el nuevo). Persistente en todos → mirar el healthcheck, que es el caso de arriba.
Yo di por bueno «era el deploy» tras verlo pasar una vez, y el 404 volvió: el `curl` iba al
apex y el navegador al `www`.
