---
name: dokploy-webhook-independiente-del-ci-status
description: Dokploy despliega al recibir push del webhook git, no espera al CI — un CI bloqueado/rojo no detiene el deploy
date: 2026-05-21
source: claude-code-session
tags: [dokploy, ci, github, deploy]
metadata:
  type: feedback
---

Dokploy escucha el **webhook git de push** y arranca el deploy de inmediato. No mira el estado de GitHub Actions / cualquier CI externo. Consecuencias:

- Si CI está bloqueado por billing/cuota/falla de runner, **el deploy sigue funcionando** al pushear a la rama configurada. No hay que re-pushear ni hacer nada extra cuando arregles el CI.
- Inversamente: tener checks de CI verdes NO garantiza nada sobre el deploy — Dokploy ya lo hizo antes (build + healthcheck propios).
- Si quieres bloquear el deploy hasta que pase el CI, hay que ponerlo aguas arriba (branch protection rule "require status checks" + Dokploy escuchando solo a `main`).

Caso real 2026-05-21: org `AgentesIA-MAdrid` agotó minutos Actions, CI rojo en facturaia. Los 4 commits pusheados a main desplegaron limpio vía webhook. Ver [[github-actions-org-private-free-tier-2000-min]].
