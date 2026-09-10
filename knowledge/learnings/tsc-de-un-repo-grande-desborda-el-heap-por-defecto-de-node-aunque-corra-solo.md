---
title: tsc de un repo grande desborda el heap por defecto de node aunque corra solo
date: 2026-09-03
source: facturaia
tags: [typescript, node, git-hooks, gate, memoria]
---
`typecheck` en el pre-commit y `build` en el pre-push mueren con «FATAL ERROR: Ineffective
mark-compacts near heap limit» **sin ningún otro gate corriendo**: main de facturaia ya pide
4,26 GB / 1,67 M de tipos (`tsc --extendedDiagnostics`), justo el heap por defecto de Node.

El engaño: huele a concurrencia entre sesiones, se espera media hora al «cerrado» del vecino, y
vuelve a morir igual. Es tamaño del repo, no carga de la máquina.

Fix: `export NODE_OPTIONS=--max-old-space-size=8192` en el `zsh -c` del `nohup` que lanza el
commit o el push; los hooks lo heredan y no se salta ninguna etapa. Con 8 GB por proceso siguen
sin caber dos gates en 16 GB, así que el semáforo de un gate por vez se mantiene. Medido con la
sesión vecina el 3-sep-2026.

Ver [[turbopack-rechaza-symlink-node-modules-en-worktree]] · [[facturaia]]

**Ampliación 10-sep-2026: hay DOS muertes distintas y el fix de arriba causa la segunda.**
`Ineffective mark-compacts` es V8 quedándose sin su heap. **SIGTERM es el kernel matando el
proceso** porque la máquina no tiene memoria: 16 GB con swap a 11,3 de 12 GB, y el hook lo
imprime como «Commit bloqueado: errores de TypeScript». Tercera misatribución de la misma
familia: el mensaje del hook nunca dice la causa, la línea de encima sí (`terminó con código
SIGTERM`).

Y el `export NODE_OPTIONS=--max-old-space-size=8192` ya no es el remedio sino el amplificador:
desde el 3-sep los scripts inyectan el heap solos, y exportarlo lo hereda `vitest` con
`maxWorkers` 5 — cinco techos de 8 GB donde antes había uno.

**El instrumento de espera también estaba mal.** Armé un reintento condicionado a `load < 14`:
el load mide la cola de ejecución, no la memoria. Bajó de 14, disparó, y `tsc` murió igual con
el swap a 11,3/12. Lo que discrimina es `sysctl vm.swapusage` (esperar swap libre, no carga
baja) y, antes de eso, cerrar lo propio que sigue residente — un `next dev` olvidado devolvió
500 MB.

Ver [[el-porcentaje-de-swap-no-discrimina-thrashing-los-swapouts-si]]
