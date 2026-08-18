---
title: rebase/cherry-pick --continue estripa del mensaje toda línea que empiece por `#`
date: 2026-08-18
source: claude-code-session
tags: [git, rebase, convenciones, mensajes-de-commit]
---
`git rebase --continue` y `git cherry-pick --continue` pasan por el editor, y ahí git aplica
`cleanup=strip`: **borra toda línea que empiece por `#`**, tratándola como comentario. En repos cuya
convención de asunto es `#NNN — descripción` (agh-iberica) eso **se come el asunto entero** y con él la
referencia al issue. Sin error y sin aviso: el commit se crea y parece correcto.

Medido dos veces la misma tarde: un cherry-pick dejó como asunto una frase del medio del cuerpo; un
rebase se llevó **seis** líneas.

- Solo ocurre **con conflicto** (sin conflicto no hay editor), o sea justo cuando estás en otra cosa.
- Detección: `git log -1 --format='%s'` después de CADA `--continue`.
- Fix: `git log -1 --format='%B' <sha-original> > /tmp/m.txt && git commit --amend --cleanup=verbatim -F /tmp/m.txt`.
  El `--cleanup=verbatim` es lo que importa: sin él el amend vuelve a estriparlo.
- Prevención: `git config commit.cleanup whitespace` en repos con esa convención de asunto.

Ver [[rebase-onto-pr-stackeada-squash-no-duplicar]] · [[tres-puntos-y-git-cherry-mienten-en-ramas-squash-mergeadas]]
