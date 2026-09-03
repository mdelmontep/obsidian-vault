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
