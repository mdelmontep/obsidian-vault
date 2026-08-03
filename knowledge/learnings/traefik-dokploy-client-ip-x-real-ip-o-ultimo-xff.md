---
title: bajo traefik/dokploy la ip del cliente está en x-real-ip o último xff (no primero)
date: 2026-05-26
source: claude-code-session
tags: [dokploy, traefik, security, rate-limit]
---

Para rate-limit por IP no leer `xff.split(',')[0]` — el cliente puede spoofear el primer elemento añadiéndolo a mano. Traefik añade su propio valor al FINAL del XFF y fija `x-real-ip` con la IP del socket TCP.

Patrón seguro:
1. `x-real-ip` primero
2. fallback `xff.split(',').pop().trim()` (último elemento — el que añadió el proxy)
3. fallback `'unknown'`

Solo válido si confías en el proxy (true en Dokploy/Traefik por defecto). Aplica también a IPv6 (no asumir IPv4). Sin esto el rate-limit por IP es bypass trivial — atacante manda `X-Forwarded-For: 1.2.3.4` distinto en cada request.

Reincidió en TuFacturaIA: 4 endpoints públicos (`check-available`, `revoke-change`, `fiscal/shared/comments`, `feedback-action/resolve`) seguían con `xff[0]` 3 semanas después. Fix de origen (PR #341): helper único `src/lib/http/client-ip.ts` — single source of truth para que no se vuelva a copiar el patrón malo. Distinguir IP-rate-limit (debe ser confiable) de IP-audit-log (XFF[0] informativo, aceptable, no tocado).

**Ampliado 3-ago-2026 (TuCRMIA).** Dos cosas que faltaban:
- «El último» sólo vale con UN proxy. Generaliza a **contar N saltos desde la derecha**, con N =
  proxies propios: el día que haya un CDN delante de Traefik, «el último» es el CDN y todos los clientes
  comparten cubo. Un número de saltos se mantiene solo; una allowlist de IPs de proxy hay que mantenerla.
- En el **App Router de Next no existe `request.ip`**: un route handler recibe una `Request` y no ve el
  socket. La IP sale sí o sí de una cabecera, así que la decisión de confianza no se puede evitar.
- Qué hacer con la IP no identificable: **cubo compartido**, ni denegar (tumba local y dev, y el arreglo
  de urgencia es quitar el control) ni saltarse el contador. Y registrarlo: en el despliegue ese cubo no
  se usa nunca, así que si empieza a contar, eso es la señal de que el proxy se rompió.
- Y sobre QUÉ contar: [[un-limite-por-ip-que-cuenta-todas-las-peticiones-anula-el-limite-por-credencial]]

