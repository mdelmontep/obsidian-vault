---
title: cambio de dominio no es migración — verificar backend antes de asumir
date: 2026-05-19
source: claude-code-session
tags: [infra, dns, integraciones, debugging]
---

Cuando un equipo dice "migramos de X a Y" verificar **antes** que es la misma BD/backend. Caso: `facturaia.agentesia.world` → `app.tufacturaia.com` se documentó como "migración" pero era solo nuevo dominio sobre la misma Supabase. Integraciones (portal con `FACTURAIA_API_URL=…agentesia.world`) quedaron apuntando al dominio caído durante semanas — todas las llamadas fallaban silenciosamente con 404.

**Checklist al oír "migramos":**
1. ¿La BD nueva tiene los mismos org_id / IDs? Si sí → no es migración real, es rebranding.
2. ¿El cliente HTTP del consumidor sigue funcionando? Probar con `curl -I` al dominio viejo.
3. ¿Coincide el prefijo API? TuFacturaIA cambió de `/v1/*` a `/api/v1/*` con el dominio nuevo — el cliente HTTP del portal añadía `/api/v1` igual, pero el endpoint viejo era distinto.
4. Buscar en repos consumidores `grep -rn DOMINIO_ANTIGUO` antes del rebranding para crear lista de envs a actualizar.

**Pista de detección a posteriori:** integraciones que fallan con 404/timeout en endpoints que antes funcionaban → primer check es el dominio + comparar con el repo origin.
