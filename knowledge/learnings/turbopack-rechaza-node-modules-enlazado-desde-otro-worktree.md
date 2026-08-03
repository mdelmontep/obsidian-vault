---
title: turbopack rechaza un node_modules enlazado desde otro worktree
date: 2026-08-03
source: claude-code-session
tags: [nextjs, turbopack, git-worktree, gates]
---
Un `git worktree` nuevo no tiene `node_modules`, así que el `pre-push` que corre `build` falla aunque el
cambio sea de documentación. El atajo obvio —`ln -s ../repo/node_modules`— **no vale con Turbopack**:

```
FATAL: Symlink [project]/node_modules is invalid, it points out of the filesystem root
```

Panic, no error recuperable. Turbopack ancla un *filesystem root* y rechaza cualquier symlink que
apunte fuera; da igual que el `package-lock.json` sea idéntico. Tampoco sirve `--no-verify`: saltarse
el gate por comodidad es justo lo que el hook existe para impedir.

Salida real: `npm ci --prefer-offline --no-audit --no-fund` dentro del worktree (~2 min con caché
caliente, ~1 GB). Presupuéstalo al abrir un worktree que vaya a empujar, junto con copiar `.env.local`
(tampoco lo hereda, y el build lo necesita).

Lo que lo hace confuso (03-ago): **`vitest`, `tsc --noEmit` y `eslint` sí resuelven con el symlink**.
Puedes tener tests, tipos y lint en verde y creer que el worktree está montado; solo revienta al
llegar al `build` o al levantar `dev`. Si vas a mirar algo en el navegador, el `npm ci` no es opcional.

Ver [[limpiar-root-checkout-viejo-con-worktrees-stash-selectivo-ff-only]]
