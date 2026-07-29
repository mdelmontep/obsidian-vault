---
title: el reaper de fia-gate mata typecheck/build en background de otras sesiones
date: 2026-07-29
source: claude-code-session
tags: [claude-code, harness, fia-gate, background, macos]
---

`reap_orphans()` de `~/.claude/gate/fia-gate` mata (`killtree`) todo proceso que case
`node_modules/.bin/{tsc,next,eslint,stylelint}` **y tenga PPID 1**, con la premisa "un proceso
legítimo siempre tiene padre vivo". Es falsa con varias sesiones: un `run_in_background` del
harness acaba reparentado a launchd (PPID 1) aunque el trabajo esté vivo → cada vez que OTRA
sesión arranca un job, el gate hace limpieza y se lleva el tuyo por delante.

Síntoma: el job llega como `killed`/`stopped`, log vacío o cortado a mitad, sin error ni OOM, a
los pocos segundos. Parece [[background-bash-io-bound-se-mata-solo-reintentar]] pero aquí la
causa es real y reintentar no basta (4 intentos seguidos muertos).

Fix inmediato: invocar por la ruta real, que no casa el patrón —
`node ./node_modules/typescript/bin/tsc --noEmit`, `node ./node_modules/next/dist/bin/next build`.
Fix de fondo: marcar los procesos propios (env del gate) y reapear solo los NO marcados.

Caso: FacturaIA 2026-07-29, gate del merge de #1326/#1327. Ver [[fia-gate]].
