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
