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
(== main; gotcha del retarget). El squash deja en main el ÁRBOL exacto de la base, así que
si nadie mergea entre medias el `--onto` no cambia el árbol de la apilada (`HEAD^{tree}` igual):
su gate, corrido en paralelo sobre la base, sigue valiendo. Si main se movió, re-gate (1-oct-2026).
