---
title: pre-commit/pre-push lentos en repo compartido — lanzar en background y hacer poll
date: 2026-07-02
source: claude-code-session
tags: [git, hooks, claude-code, workflow]
---

`git commit`/`git push` con hooks pesados (lint+typecheck+build) pueden
colgarse 2-5 min sin error real cuando otra sesión de Claude Code trabaja
en paralelo en el mismo repo/máquina — es contención de CPU, no un fallo
del hook. Dejar que el timeout del tool mate el proceso a mitad es peor:
deja lockfiles/builds huérfanos (`.next/lock`) que rompen el siguiente
intento con un error engañoso (ver [[next-build-lock-huerfano-hace-fallar-pre-push-hook]]).

Fix: lanzar el comando en background (`nohup git commit -m "..." > /tmp/log 2>&1 &`,
guardar el PID) y esperar con un poll (`while ps -p $PID >/dev/null; do sleep 5; done`)
en vez de un timeout corto que lo interrumpe. Deja que el hook termine a su ritmo.
