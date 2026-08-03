---
title: el parte de un job caído no es evidencia de lo que dejó
date: 2026-08-03
source: claude-code-session
tags: [agentes, runner, verificacion, facturaia]
---

Un job del ticket-runner agotó los 30 min (`JOB_TIMEOUT_MS`) y dejó dos afirmaciones sobre sí mismo. Las dos falsas, en direcciones opuestas:

- **Prometió un artefacto que no existe.** Su `error` decía «la sesión SÍ alcanzó a volcar su análisis... está en el hilo interno del ticket». El mensaje del hilo era literalmente `Execution error`, 15 caracteres.
- **Se infravaloró.** Commiteó el rescate como `wip(...) (sin terminar)`, y auditado en un worktree el trabajo estaba **completo**: typecheck y lint limpios, 1.570 tests en verde con 43 nuevos, los tres puntos del ticket implementados con guards y auditoría. Rehacerlo habría tirado 1.867 líneas verificadas.

Regla: ante un job caído, **auditar la rama antes de decidir**, y no dar por escrito nada que el propio job diga de su resultado. El relanzamiento sale mucho más barato como *continuación* (fusionar la rama de rescate + alcance solo de cierre) que como reintento desde cero, que además vuelve a chocar con el mismo techo de tiempo.

Corolario del techo: si el timeout vive en el compose de Dokploy y no puedes subirlo, la única palanca es **estrechar el alcance del prompt**, no reintentar igual.

Ver [[autodeploy-sin-watchpaths-mata-el-trabajo-en-vuelo-del-worker]] · [[stash-o-wip-viejo-puede-estar-ya-en-main-verificar-antes-de-reconciliar]]
