---
title: request.url detrás de un proxy trae el host interno, y el redirect acaba en 0.0.0.0
date: 2026-08-03
source: claude-code-session
tags: [next, traefik, dokploy, auth, despliegue]
---
En un route handler de Next detrás de Traefik, `new URL(request.url).origin` es el host **interno del
contenedor**: el redirect sale como `Location: http://0.0.0.0:3000/login`. En local es invisible porque
los dos hosts coinciden — solo se ve llamando a la ruta desplegada.

Caso real: el callback del enlace de acceso. El usuario gastaba su enlace de un solo uso para acabar en
una dirección que no existe fuera del contenedor.

Fix: **`Location` relativo** (`new Response(null, {status, headers:{Location:'/login'}})`), que resuelve
el navegador contra el origen que ya usa (RFC 9110 §10.2.2). No hay nada que adivinar.

**No** leer `X-Forwarded-Host`: la escribe quien esté delante, así que construir un destino con ella es
dejar que otro elija a dónde van tus usuarios. `NextResponse.redirect` no sirve: exige URL absoluta.
Guard barato: rechazar destinos que no empiecen por una sola barra (`//otro.com` es otro dominio).
