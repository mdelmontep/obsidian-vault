---
title: en un git worktree `.git` es un FICHERO — detectar la raíz con existsSync devuelve la rama, no el repo
date: 2026-07-25
source: claude-code-session
tags: [git, worktree, hooks, telemetria, agency-portal]
metadata:
  type: learning
---

Detectar la raíz de un repo subiendo directorios hasta `existsSync(join(dir, '.git'))` y devolver `basename(dir)` funciona en un clon normal y falla en silencio en un **worktree**: ahí `.git` no es un directorio, es un fichero de una línea (`gitdir: <repo>/.git/worktrees/<nombre>`). El bucle corta en el propio worktree y el "nombre del repo" acaba siendo el nombre de la carpeta del worktree, que en la práctica es la rama.

Efecto real (hook de time-tracking, agency-portal): 5 sesiones de Claude Code del mismo repo se reportaron como 3 proyectos (`facturaia`, `modia-003-escape-stack`, `importe-cobrable-retenciones`) y el panel "Trabajando ahora" solo mostraba 3 de 5. Sin error, sin log: datos fragmentados que parecen correctos.

**Fix**: si `statSync(gitPath).isFile()`, leer el fichero y sacar el repo principal del `gitdir:` (`/^gitdir:\s*(.+?)[/\\]\.git[/\\]worktrees[/\\]/` → `basename($1)`). De paso agrupa bien los worktrees hermanos fuera del repo (`facturaia-sepa`).

Aplica a cualquier script que derive identidad de proyecto del cwd (hooks, telemetría, statuslines, CI local). Backfill del histórico con lista literal de valores, verificados en BD. Hermano de [[identificador-de-carpeta-local-diverge-entre-maquinas-normalizar-en-ingesta]].
