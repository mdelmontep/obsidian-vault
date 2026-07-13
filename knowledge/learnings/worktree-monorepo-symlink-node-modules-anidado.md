---
title: worktree fresco de monorepo — el symlink de node_modules debe incluir el de cada paquete anidado
date: 2026-07-13
source: claude-code-session
tags: [worktree, monorepo, node, testing]
---
Al aislar trabajo en `git worktree add` y enlazar `node_modules` del checkout raíz para no reinstalar:
el symlink de la RAÍZ NO basta si el repo es monorepo con un subpaquete que tiene su PROPIO
`node_modules` (caso AGH: `dashboard/node_modules`). Sin él, los tests de ese subpaquete fallan con
`Failed to load url react/jsx-dev-runtime … Does the file exist?` (o similar de resolución) → parece
una regresión de TU cambio y no lo es (artefacto del symlink incompleto: el gate marca 8 suites en rojo
por un cambio que era SQL puro).
Fix: un symlink por cada paquete con deps propias —
`ln -s <root>/node_modules node_modules` **y** `ln -s <root>/dashboard/node_modules dashboard/node_modules`.
Al commitear, añadir SOLO por ruta (`git add <ficheros>`) para no arrastrar los symlinks.
Ver [[triaje-seguro-ramas-worktrees-sesiones-paralelas]].
