---
title: turbopack rechaza un node_modules enlazado fuera del worktree; copiar con cp -cR
date: 2026-10-01
source: facturaia (PR #3196, gate en worktree)
tags: [nextjs, turbopack, git-worktree, macos]
---
- Enlazar `node_modules` del checkout principal en un worktree (`ln -s`) va bien para lint, tsc y vitest, y el gate solo revienta en la ÚLTIMA etapa, `next build`: `TurbopackInternalError: Symlink [project]/node_modules is invalid, it points out of the filesystem root`.
- Coste real: la suite entera (~5 min) corre en verde antes de descubrirlo.
- Fix: copia APFS copy-on-write, instantánea y sin ocupar disco: `cp -cR <principal>/node_modules ./node_modules`, solo si `package-lock.json` es idéntico.
- Para medir solo con `tsc` (tarea semanal de volumen de tipos) el enlace sí vale.
