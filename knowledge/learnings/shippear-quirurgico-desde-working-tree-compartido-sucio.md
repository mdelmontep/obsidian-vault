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

Gotchas (TuFacturaIA 12-jun): la paralela puede commitear tu trabajo uncommitted
y renumerar tu migración (`43fae46`, 252→254) — re-verificar `status`/`ls-files`/`log`
antes de "limpiar duplicados"; y re-correr lint/typecheck/build EN el worktree.

**Si son 1-2 ficheros, el worktree sobra: plumbing** (23-ago, cambio de una línea de doc).
`git hash-object -w <f>` → índice temporal (`GIT_INDEX_FILE=… read-tree origin/main` +
`update-index --cacheinfo`) → `write-tree` → `commit-tree -p origin/main` → `update-ref` →
push. No toca HEAD, ni el índice real, ni el árbol del otro; el `pre-push` sí corre porque
sale del checkout que ya tiene `node_modules` (en un worktree nuevo muere en `vitest: command
not found`). Luego devolver el fichero con una **edición inversa**, no `git checkout --`.
Avisar por SendMessage de qué `M` del `git status` es tuyo: la paralela commitea con `-a`.
