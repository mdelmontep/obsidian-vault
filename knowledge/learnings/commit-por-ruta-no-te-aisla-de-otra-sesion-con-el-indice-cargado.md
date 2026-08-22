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

**Y `git worktree add` tampoco aísla si dos sesiones eligen el MISMO worktree** (22-ago, facturaia,
cinco sesiones vivas). Pasó dos veces la misma tarde: en `wt-arnes` la otra sesión commiteó mis
ficheros sin commitear dentro de su commit, y en `wt-aeat-1934` un subagente vio el `md5` de la
migración cambiar entre dos muestras sin haberla tocado. El coste no fue la autoría: fueron **dos
implementaciones del mismo encargo**. Lo que aísla es un worktree por sesión, no por rama — antes de
escribir, `lsof -a -d cwd +D <worktree>` y mtimes de minutos.

Señales de sesión viva antes de tocar nada: `git status` con ficheros que no son tuyos, y **mtimes de
hace segundos** (`find . -newermt '-3 minutes'`). Ver [[git-worktree-por-sesion-paralela]].
