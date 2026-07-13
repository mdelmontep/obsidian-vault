---
title: pr stackeada sobre otra con squash-merge — rebase --onto <base-vieja>, no rebase normal
date: 2026-07-13
source: claude-code-session
tags: [git, github, pr]
---
Al mergear con SQUASH la PR base, su commit entra en main con un SHA NUEVO. La PR
stackeada encima aún tiene el commit ORIGINAL de la base → un `git rebase origin/main`
normal lo reaplica y DUPLICA (o conflicta).

Fix: `git rebase --onto origin/main <sha-base-original> <rama-stackeada>` → reaplica solo
los commits PROPIOS de la stackeada sobre el main que ya lleva la base dentro.

Después, antes de mergear: `gh pr edit <n> --base main` + `gh pr view <n> --json baseRefName`
(== main; gotcha del retarget) y re-correr el gate sobre el HEAD rebasado.
