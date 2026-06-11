---
title: shippear quirúrgico desde working tree compartido sucio
date: 2026-06-12
source: claude-code-session
tags: [git, worktree, sesiones-paralelas]
---
Working tree compartido con sesión paralela (staged ajeno + conflictos `UU`) → nunca commitear ahí.

Patrón: worktree desde `origin/main` + por cada archivo modificado `git diff origin/main HEAD -- <file>`:
- diff 0 → la copia del working tree es segura wholesale (base idéntica, solo tus cambios).
- diff ≠ 0 (caso `globals.css` con glass staged) → re-aplicar solo tu hunk a mano en el worktree.

Gotchas (caso real TuFacturaIA 2026-06-12, feature tickets feedback):
- La sesión paralela puede **commitear tu trabajo uncommitted** y renumerar tu migración (`43fae46`, 252→254). Al volver, re-verificar con `git status` + `git ls-files` + `git log` antes de "limpiar duplicados" — pueden ya no existir o estar tracked.
- Duplicados untracked idénticos a main bloquean merges futuros ("would be overwritten by merge") si nadie los commitea.
- Re-verificar lint/typecheck/build EN el worktree (el contenido difiere del branch donde testeaste).
