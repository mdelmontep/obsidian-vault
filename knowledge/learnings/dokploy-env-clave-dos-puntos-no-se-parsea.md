---
title: env de dokploy con CLAVE:valor (dos puntos) no define la variable
date: 2026-05-27
source: claude-code-session
tags: [dokploy, docker, infra]
---

En la pestaña Environment de Dokploy una línea `NEXT_PUBLIC_SITE_URL:https://x`
(dos puntos) NO define la variable — Docker/Dokploy parsea `CLAVE=VALOR`, y una
línea con `:` se ignora en silencio. El contenedor arranca sin esa env y el
código cae a su fallback (en FacturaIA: derivaba la URL del header `host` →
`0.0.0.0:3000`, el bind interno → enlaces de invitación inalcanzables).

Síntoma: la var "está" en el panel pero ausente en runtime.

Verificar SIEMPRE con `compose.one` (API Dokploy) o `docker exec X env | grep CLAVE`,
nunca confiar en el editor del panel. Caso 2026-05-27: invitaciones rotas porque
2 `NEXT_PUBLIC_*` tenían `:`. Hermano de [[dokploy-paste-compose-corruption]].
