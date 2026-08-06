---
title: limpiar un root checkout viejo con worktrees paralelos — stash selectivo + ff-only, nunca reset
date: 2026-07-13
source: claude-code-session
tags: [git, worktrees, claude-code]
---
Root checkout con el HEAD atrás y cambios sin commitear, rodeado de N worktrees paralelos:

- **NO** `reset --hard`/checkout forzado: el git-guard lo bloquea (protege los worktrees) y es destructivo.
- **Caracteriza los cambios antes de descartar**: ¿obsoletos (ya superados por origin/main) o WIP real? Señal de obsoleto: el working tree RE-INFLA un archivo que un refactor ya mergeado adelgazó (caso real: `app.ts` monolito de 690 líneas pre-split #455 vs `app.ts` fino de 340 en main → arqueología, no trabajo).
- **Limpieza sin pérdida**: `git stash push -m "..." -- <paths>` (selectivo → deja untracked como `.claude/` intacto; 100% recuperable con `stash pop`), NUNCA `restore`/`reset`.
- **HEAD al día**: `git merge --ff-only origin/main` — el git-guard SÍ permite un fast-forward LIMPIO (no reescribe historia), aunque bloquee los HEAD-moves destructivos.

**Un árbol sucio de varios días puede ser una MEZCLA, no un veredicto único.**
Caso real (06-ago, 3 días sin commitear, 56 ficheros): una parte era una versión
anterior y con bugs de trabajo ya mergeado (descartable, verificado archivo a
archivo contra el comentario del propio código en `origin/main` explicando por
qué su versión es la correcta — contraste AA, orden de providers, etc.), y OTRA
parte, mezclada en el mismo `git status`, era una feature completamente
DISTINTA y real (un componente nuevo sin ningún equivalente en main). Un
veredicto "todo obsoleto" habría tirado trabajo real; "todo se rescata" habría
mergeado un bug ya corregido.

Flujo que sí escala a esto: `git stash push -u` (todo, incluidos untracked) →
`git pull --ff-only` en el root limpio → `git stash pop` (los conflictos reales
son la señal de qué SÍ cambió en los dos sitios; lo que aplica limpio sin
conflicto ya lo decidió el 3-way merge) → resolver cada conflicto mirando el
comentario/evidencia de la versión de main, no por volumen ni por "parece
igual" → **mover todo el resultado a worktree+rama nueva** (nunca commitear
en el root con HEAD compartido) → correr el gate completo → **partir en
commits atómicos por grupo temático**, no un commit-mochila.
