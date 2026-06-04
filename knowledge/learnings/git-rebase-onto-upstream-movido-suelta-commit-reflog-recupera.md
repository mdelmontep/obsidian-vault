---
title: rebase --onto sobre upstream movido puede soltar tu commit; reflog + cherry-pick recupera
date: 2026-06-05
source: claude-code-session
tags: [git, sesiones-paralelas]
---
Sesión paralela en el mismo repo: otra sesión commiteó a TU local main → tu
rama feature quedó encima de ese commit ajeno. Al rebasar para soltarlo
(`git rebase --onto origin/main <commit-ajeno> mirama`) con origin/main ya
avanzado (el ajeno mergeado por squash), el rebase dijo "Successfully rebased"
pero **dejó HEAD == origin/main, soltando tu commit**.
- Síntoma: `git log origin/main..HEAD` vacío + `git diff origin/main` vacío +
  tus archivos nuevos desaparecidos del working tree.
- Recuperación: tu commit sigue en `git reflog` (HEAD@{2}); `git reset --hard origin/main`
  + `git cherry-pick <sha-del-reflog>` lo reaplica limpio (diff disjunto).
- Prevención: tras CUALQUIER rebase, verifica `git log origin/main..HEAD` ANTES
  de push. Y no construyas ramas sobre un local main con commits sin pushear de
  otra sesión.
