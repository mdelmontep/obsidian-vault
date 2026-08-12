---
title: turbopack build rechaza node_modules symlink en un worktree
date: 2026-08-13
source: claude-code-session
tags: [nextjs, turbopack, worktree, build]
---

`ln -s <repo-raiz>/node_modules` en un worktree nuevo es el atajo obvio para no
copiar ~1,2 GB, y `lint`, `tsc` y `vitest` funcionan — pero `next build`
(Turbopack, Next 16) revienta con `FATAL: Symlink [project]/node_modules is
invalid, it points out of the filesystem root`. Turbopack resuelve el symlink
fuera de la raíz del proyecto y lo rechaza entero.

Fix: copia real (`cp -R`, ~30 s en APFS) o `npm ci` en el worktree. El symlink
solo vale si ese worktree nunca va a correr el build — y el gate pre-PR de la
casa siempre lo corre, así que en la práctica: copiar siempre.

Caso: worktree de contenido-06b en facturaia, 13-ago-2026.
