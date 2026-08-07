---
title: `git commit -- <ruta>` no te aísla si otra sesión tiene el índice cargado en el mismo checkout
date: 2026-08-07
source: claude-code-session
tags: [git, sesiones-paralelas]
---
Dos sesiones en el MISMO checkout. La otra deja ficheros en el índice (`git add`) y se queda pensando.
Tú commiteas por ruta para no llevarte lo suyo:

```
git commit -m "…" -- docs/mi-fichero.md
```

Correcto y no basta: el pathspec protege **tu** commit, pero tu fichero queda en el árbol de trabajo y,
si la otra sesión commitea primero, **su `git commit` se lo lleva dentro con su mensaje**. Pasó: mi
documento acabó en un commit ajeno. No se pierde nada, pero la autoría y el mensaje son de otro, y el
commit dice algo distinto de lo que contiene.

**Lo único que aísla de verdad es no compartir el checkout**: `git worktree add` por sesión. El
pathspec es un parche para cuando ya estás dentro.

Señales de sesión viva antes de tocar nada: `git status` con ficheros que no son tuyos, y **mtimes de
hace segundos** (`find . -newermt '-3 minutes'`). Ver [[git-worktree-por-sesion-paralela]].
