---
title: node_modules por symlink en un worktree rompe el build de turbopack
date: 2026-07-29
source: claude-code-session
tags: [next, turbopack, worktree, gate]
---

Atajo tentador al abrir un `git worktree`: `ln -s <repo>/node_modules <worktree>/node_modules` para
no esperar un `npm ci`. **Vitest, eslint y `tsc` funcionan; `next build` no.**

```
Symlink [project]/node_modules is invalid, it points out of the filesystem root
  type: 'TurbopackInternalError'
```

Turbopack resuelve rutas contra la raíz del proyecto y rechaza un symlink que apunta fuera de ella.
El fallo aparece tarde y confunde: el gate pre-push muere en `build` con un error de infraestructura
que se lee como error de código, después de que lint/typecheck/tests hayan pasado.

En un worktree que vaya a pasar el gate completo, `npm ci` de verdad desde el primer momento. El
symlink solo vale para worktrees de solo-lectura (leer código, correr un test suelto).

Ver [[claude-code-agentes-worktree-failure-modes]] · [[fia-gate-watchdog-mata-la-cadena-entera-con-un-solo-presupuesto]]
