---
title: rebasar un worktree deja node_modules caduco, y el gate no lo distingue de instalado
date: 2026-08-06
updated: 2026-08-07
source: claude-code-session
tags: [worktrees, gate, npm, verificacion]
---
Worktree por issue + rebase antes de mergear = **el flujo normal genera worktrees con las
dependencias caducas**. `node_modules` existe (así que un preflight de existencia calla), pero se
instaló contra el `package.json` de ANTES del rebase: si algún merge intermedio añadió una
dependencia, el typecheck revienta con `TS2307: Cannot find module …` y el gate muere sin llegar a
correr los tests. El mensaje que sale («murió antes de arrancar») es cierto y **no nombra la causa**.

Coste real: 3 corridas de gate perdidas en un tren de 7 merges (AGH, 6-ago).

- **`npm ci` va DESPUÉS del rebase, nunca antes** — instalar primero y rebasar después es
  exactamente el orden que produce el fallo.
- Y en cada proyecto del gate, no solo la raíz (aquí faltaban `playwright` y un paquete de Radix,
  los dos en `dashboard/`).
- La comprobación barata que lo caza: `mtime` de `package-lock.json` contra
  `node_modules/.package-lock.json` — npm escribe el segundo en cada instalación.
- **7-ago: implementada en el preflight del gate (AGH PR #1062).** Cuando entre, esta entrada puede
  salir de `hot.md`: pasa a estar bloqueada por una máquina. Dos matices que costaron medirlos —
  el **sello ausente cuenta como caduco** (npm ≥7 siempre lo escribe; si falta, ese árbol no lo
  instaló npm ahí — el `ln -s` al `node_modules` de otro proyecto, que dio 3 rojos fantasma), y la
  pista tiene que ser **distinta** de la de «no instalado» o separar los dos estados no sirve de nada.

Relacionado: [[worktree-monorepo-symlink-node-modules-anidado]] ·
[[auditar-sobre-origin-main-worktree-no-cwd-stale]].
