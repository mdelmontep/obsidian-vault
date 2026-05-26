---
title: confirmar estado real del PR antes de invertir en review
date: 2026-05-05
source: claude-code-session
tags: [git, github, workflow, code-review]
---

Antes de actuar sobre items de una review, confirmar (a) que el PR sigue abierto y (b) que el head no ha cambiado desde el review submit. `gh pr view <n> --json state,mergedAt,headRefOid` + `git log origin/<rama> -5`. Mapear cada item ↔ commit antes de tocar nada — reactuar sobre items ya resueltos = revertir trabajo y arrastrar conflictos al rebase.

Señales de stale:
- Reviewer dice en chat "lo arreglé yo" pero GitHub aún muestra "Changes requested"
- Commits del reviewer en la rama posteriores al review submit
- `gh pr list --state open` cachea: un PR mergeado puede seguir apareciendo OPEN minutos/horas

Caso 1 (PR #54 agency-portal, 2026-05-05): Borja posteó 4 bloqueantes, los aplicó él mismo en `58e0ef0` y cambió la base. Review siguió visible, solo quedaba 1 cosa nuestra.

Caso 2 (PR #75 TuFacturaIA, 2026-05-26): `gh pr list --state open` devolvió cacheado un PR ya mergeado hace 3h. Hice review completa, hallé "regresión bloqueante en bancos-section" → al verificar contra `git show <merge-commit>` resulta que el rebase manual del propio user ya lo había arreglado. Comment quedó posteado en PR cerrado, inútil.
