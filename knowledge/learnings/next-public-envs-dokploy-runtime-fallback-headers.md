---
name: next-public-envs-dokploy-runtime-fallback-headers
description: NEXT_PUBLIC_* envs Dokploy a veces no propagan al runtime — fallback al host del request
metadata:
  type: feedback
---

En Next.js standalone deployado vía Dokploy, las envs `NEXT_PUBLIC_*` que están configuradas en el panel a veces NO llegan al runtime del container (problema build vs runtime, propagación entre capas, manifest no aplicado). Síntoma: `process.env.NEXT_PUBLIC_SITE_URL` undefined aunque el panel dice que está set.

**Why:** Caso real 2026-05-20 — `/api/team/members` daba "server_misconfigured" por falta de `NEXT_PUBLIC_SITE_URL` aunque estaba en el panel. Tras múltiples redeploys, ninguna propagaba.

**How to apply:** En endpoints server-side que necesiten la URL del sitio:
1. Aceptar varios nombres de env como fallback (`NEXT_PUBLIC_SITE_URL || NEXT_PUBLIC_APP_URL`).
2. Si ninguno, derivar del request: `${req.headers.get('x-forwarded-proto') || 'https'}://${req.headers.get('x-forwarded-host') || req.headers.get('host')}`. Traefik añade esos headers automáticamente.

Este patrón es válido para cualquier endpoint que solo necesite la URL "del sitio donde el user está ahora" (links de redirect, magic links, callbacks). NO usar para validar firmas o policies de allowlist — para eso necesitas env explícita.

Ver [[Stack/docker-infra]] §"Dokploy" para diagnóstico envs runtime.
