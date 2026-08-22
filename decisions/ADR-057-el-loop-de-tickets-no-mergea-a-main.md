---
title: ADR-057 — el loop de tickets abre PR y no mergea a main
date: 2026-08-22
tags: [adr, facturaia, harness, loop, ci]
---

## Contexto
`scripts/loop-tickets.sh` arranca una sesión de Claude por ticket. Traía `--merge`, que
mergeaba a `main` si su `gate()` local salía verde. No hay CI (billing de Actions caído
desde el 17-jun) ni branch protection (`gh api …/rulesets` → 403, requiere Pro).

## Opciones
1. **Parchear el gate y conservar `--merge`.** Su guard de `__integration__` usaba
   `git diff` antes de existir el commit, así que no veía ficheros sin trackear: un ticket
   que AÑADÍA un test ahí pasaba en verde.
2. **Publicar sin `--merge`** — el script se queda en «worktree + gate + PR».

## Decisión
Opción 2, y el guard endurecido igualmente (`:(glob)`, `ls-files --others`, `__evals__`).

## Porqué
El parche arregla el guard pero no el defecto de fondo: **no existe un «HEAD validado»**.
El gate mide el árbol y el commit es posterior; `deps:json` reescribe un fichero tracked
entre medias, y `mig:renumerar` muta, commitea y pushea **después** del gate. Sin CI ni
protección de rama, un squash a `main` es irreversible en la práctica, y lo que compra es
sólo «desbloquear el frente solo». Ver [[gate-en-segundo-plano-no-incluye-los-trinquetes-del-pre-commit]]

## Consecuencias
El loop deja PRs para revisión humana. Si algún día se quiere `--merge`: gate **después**
del commit y del renumerado, `--match-head-commit` del SHA gateado, cwd distinto del
checkout compartido y `MAX` por defecto a 1. PR #2105.
