---
title: git stash sin -u deja untracked en disco y el hook pre-commit los detecta
date: 2026-06-23
source: claude-code-session
tags: [git, hooks, build]
---

`git stash` sin `-u` no toca archivos untracked — siguen en disco.

Si el hook pre-commit escanea el directorio y auto-añade imports (ej. auto-registry de email templates), el import entra al staged file pero el tipo correspondiente no está en git → build falla con "Module not found" o error TS.

**Fix:** `git stash -u` cuando hay WIP untracked que el hook puede detectar.

**Diagnóstico:** `git stash list` + `ls` del dir afectado. Si el archivo existe en disco pero no en `git status` (untracked ya guardado en stash previo sin `-u`).
