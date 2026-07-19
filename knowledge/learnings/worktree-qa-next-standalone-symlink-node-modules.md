---
title: qa visual en git worktree de un proyecto next necesita node_modules y dev (no next start con output standalone)
date: 2026-07-19
source: claude-code-session
tags: [git-worktree, nextjs, qa, playwright]
---
Para QA visual en paralelo se crea un `git worktree` desde `origin/main`, pero:

1. El worktree NO trae `node_modules` (git no lo versiona). Sin él, `npx vitest`
   coge un binario ajeno y falla (`Cannot find module 'vitest/config'`).
   Fix: `ln -s <checkout-principal>/node_modules node_modules` en el worktree
   (misma base reciente + mismo arch → seguro). Lo mismo para `.env.local`/`.env.test`
   (gitignored): copiarlos del checkout principal.
2. `next start` NO funciona con `output: 'standalone'` (avisa y sale). Para QA usar
   `npm run dev` (Turbopack) en un puerto propio (`PORT=3013`), no `next start`.
3. Playwright: un `getByText('Calendario')` puede coger a la vez el enlace del menú
   lateral (`<a>`) y el toggle de vista (`<button>`) → navega fuera. Scopear por tag:
   `locator('button').filter({hasText:/^Calendario$/})`.

Limpieza al acabar: `rm node_modules` (symlink) antes de `git worktree remove --force`.
Ver [[facturaia]].
