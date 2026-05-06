---
title: cron dokploy con docker exec curl service-key, validar con run-now
date: 2026-05-06
source: claude-code-session
tags: [dokploy, infra, cron]
---

Dokploy tiene pestaña **Schedules** dentro de cada app. Patrón estándar para llamar a un endpoint propio con service-key:

- **Service Name**: id del container destino (igual que el de la app)
- **Schedule**: cron format estándar, p.ej. `0 4 * * *` (diario a las 04:00)
- **Command**:
  ```bash
  bash -c "curl -sf -X POST URL -H 'x-service-key: $VAR'"
  ```

`-sf`: silent + fail. Falla silencioso pero exit code != 0 si el endpoint devuelve 5xx, lo cual Dokploy marca como failed schedule.

Tras crear, usar **"Run Now"** para validar:
- exit code 0
- response esperado (`{ok: true, ...}` o lo que el endpoint devuelva)

Si exit OK pero response no coincide con la lógica nueva, problema es deploy viejo, no código (ver `verificar-deploy-antes-de-debuggear-logica` o regla CLAUDE.md global).

Caso real facturaia: cron del recomendador IA `/api/internal/run-module-suggestions` con `FACTURAIA_SERVICE_KEY` inyectado vía compose `${}`. 1 sugerencia generada al primer Run Now tras redeploy.
