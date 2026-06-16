---
title: runner headless con git push dispara el pre-push hook del repo (build) → OOM
date: 2026-06-16
source: claude-code-session
tags: [git, hooks, ci, dokploy, runner]
---

Un runner/bot que clona el repo y hace `git push` hereda `core.hooksPath=.githooks`
(lo configura `npm install`/prepare). Si el repo corre `npm run build` en el pre-push
hook (gate de devs), el push del runner dispara un **segundo build** encima del que el
runner ya hizo en su gate → doble build → OOM en un contenedor con poca RAM (3G).

Síntoma engañoso: "git push falló (exit 1)" con stderr lleno de salida de Next/Node y
"allocation failure" (el OOM del hook, no del push).

Fix: el runner pushea con `git push --no-verify` (salta hooks cliente). Justificado
porque el runner ya gatea aparte y sus PRs pasan CI + review. Corolario: un orquestador
que lanza subprocesos (push, gh pr create, claude) DEBE chequear el exit code y reportar
el stderr — si no, un fallo se disfraza de éxito (reportaba `pr_abierto` sin PR real).
Ver [[postgrest-rpc-composite-devuelve-fila-de-nulls]].
