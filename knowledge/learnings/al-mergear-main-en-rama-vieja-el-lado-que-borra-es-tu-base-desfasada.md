---
title: al mergear main en una rama vieja, el lado que borra código es tu base desfasada
date: 2026-07-30
source: claude-code-session
tags: [git, merge, conflictos, pr]
---
En un conflicto de `git merge origin/main` sobre una rama antigua, el lado "incoming" que
**quita** líneas casi nunca es un cambio tuyo: es que tu base no tenía ese código todavía.
Resolver a favor del incoming revierte trabajo ajeno ya en producción, y el diff del PR lo
enseña como si fuera tuyo.

Caso: la cima de una pila de 5 PRs traía un commit "sincroniza con el árbol que pasó el
gate". Contra el `main` nuevo, ese commit borraba el trabajo del runner de otros dos PRs
(#1359, #1360) en `ai-jobs.ts`, `run-ticket.mjs` y su callback. Aceptarlo habría pasado lint,
typecheck, build y 8548 tests, porque revertir código coherente es coherente.

Regla: en un fichero que tu PR **no toca de verdad** (compruébalo con `git show --stat <sha>`
y `gh pr diff --name-only`), resuelve siempre hacia `main`.

Y para una rama apilada cuya base ya se aplastó, no mergees: reconstruye sobre `origin/main`
con el rango propio. Ver [[rebase-onto-pr-stackeada-squash-no-duplicar]] ·
[[conflicto-rebase-json-generado-regenerar-no-mergear-a-mano]].
