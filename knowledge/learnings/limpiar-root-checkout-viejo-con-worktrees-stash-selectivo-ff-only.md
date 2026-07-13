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
