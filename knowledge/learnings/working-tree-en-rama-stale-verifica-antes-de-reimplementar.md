---
title: working tree en rama stale te hace leer código viejo — verifica antes de reimplementar un follow-up
date: 2026-07-05
source: claude-code-session
tags: [git, worktrees, agentes-paralelos, evidencia-antes-de-hipotesis]
---

En un repo con **varios git worktrees** (sesiones paralelas), el working tree **principal** puede haber quedado en una **rama vieja de otra sesión** (no en `main`). Si lees el código desde ahí lo tomas por `main` y crees que un follow-up "está por hacer" cuando **ya está mergeado** → casi lo reimplementas desde cero.

Caso real (AGH #82, "cablear el exporter Langfuse"): leí `src/observability/tracing.ts` del checkout principal y era el no-op viejo → iba a construir el exporter. Estaba en una rama stale de #11; en `main` el exporter completo (`langfuse-tracer.ts`) ya llevaba mergeado desde `7241c8b`. #82 no era "construir" sino "deploy + verificación".

Fix (antes de implementar cualquier follow-up):
1. `git -C <repo> branch --show-current` — confirma en qué rama está el checkout; no asumas que es main.
2. Lee la VERDAD de main con `git show origin/main:<path>`, no del working tree.
3. `git merge-base --is-ancestor <commit> origin/main && echo EN-MAIN` — ¿el trabajo ya está mergeado?

**Y no hace falta estar en una rama ajena: en `main` también lees viejo.** El checkout principal puede
estar N commits por detrás y la métrica que usamos para «no me queda nada por subir»,
`git log origin/main..HEAD` vacía, **es ciega a eso** — mide una dirección. Lo que delata el atraso es
la contraria, `git log HEAD..origin/main`. Caso 23-ago (facturaia): el raíz estaba a 3 commits, grepeé
`src/lib/api-error.ts` y describí una versión que ya no existía; la sesión paralela cayó en lo mismo el
mismo minuto. Con worktrees vivos `git-guard` impide mover HEAD en el raíz, así que **la ceguera es
permanente, no un despiste**: para AFIRMAR qué dice un fichero de main desde ahí, `git show
origin/main:<ruta>`.

Ver [[git-diff-vs-main-drifteado-usar-merge-base]] · [[triaje-seguro-ramas-worktrees-sesiones-paralelas]] · [[pr-review-ya-resuelta-por-el-reviewer-mismo]].
