---
title: un stash/WIP viejo puede estar ya mergeado en main — verifícalo antes de reconciliar
date: 2026-07-14
source: claude-code-session
tags: [git, workflow, stash, worktree]
---
Con varias ramas mergeando en paralelo, un `stash`/WIP de hace días puede haber sido
landeado por otro PR y quedar OBSOLETO. Antes de `git stash apply` / reconciliar /
crear rama desde él:

- Coge una firma única del contenido (una línea CSS/función nueva) y
  `git log origin/main -S "<firma>" -- <fichero>`. Si aparece un commit → ya está en
  prod y el stash es basura; no lo reconcilies.
- `git apply --3way` que resulta en **cero diff** = el target ya tiene el cambio (señal
  de obsoleto). El primer intento (`patch`/`git apply` sin --3way) puede fallar por drift
  y despistar.

Caso real (TuFacturaIA): el stash "ui-glass-sidebar WIP" (8 días) ya estaba entero en
main vía `fff933e6`; monté worktree e intenté portar `globals.css` antes de detectarlo.
La nota del hub decía "en working tree" cuando llevaba una semana en prod. Fix: verificar
primero, soltar el stash, corregir la nota.
