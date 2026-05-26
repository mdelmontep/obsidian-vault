---
title: monitor deploy listo — señal de comportamiento distinto, no respuesta genérica
date: 2026-05-26
source: claude-code-session
tags: [deploy, monitoring, ops, dokploy, vercel, nextjs]
---

Para detectar "deploy completado", NO usar respuestas genéricas comunes a versión vieja y nueva: 404→200, 401 sin auth, 307→/login del middleware Next.js. **Coinciden en ambas versiones y dan falso positivo.**

Tell real: una señal cuyo COMPORTAMIENTO cambie observable entre versión vieja y nueva del MISMO endpoint:
- Endpoint A devolvía 302→`/agentes?error=...` (legacy), ahora 410 Gone (sunset) → `status_code == 410` es señal limpia.
- Endpoint B devolvía JSON `{shape:legacy}`, ahora `{shape:new}` → `jq -r .new_field` es señal.

Caso real 2026-05-26 TuFacturaIA: monitor con `POST /api/auth/email/disconnect` esperando 308 dio falso positivo al primer hit (Next middleware devuelve 307→/login en versión vieja Y nueva igual). Tuve que cambiar el monitor a `GET /api/auth/google/callback` esperando 410 (vs legacy que redirigía a `/agentes`).

Regla: antes de armar el monitor, **simular mentalmente la respuesta de la versión vieja** y confirmar que difiere de la esperada de la nueva. Si coinciden → otra señal.
