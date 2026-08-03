---
title: una rama que reescribe el mismo fichero varias veces se integra con merge, no con rebase
date: 2026-08-03
source: claude-code-session
tags: [git, merge, rebase, conflictos]
---
Rebasar N commits obliga a resolver el conflicto **una vez por commit**, y sobre estados
intermedios que nunca llegaron a existir en ninguna rama. Si el fichero en disputa lo
reescribiste 5 veces mientras `main` lo cambiaba por debajo, son 5 resoluciones inventadas
para llegar al mismo sitio.

Regla práctica: cuenta cuántos de tus commits tocan el fichero conflictivo
(`git log --oneline origin/main..HEAD -- <fichero>`). Uno o dos → rebase. Más → `git merge
origin/main`: un solo conflicto, sobre tu versión FINAL contra la de `main`, que es la única
comparación con sentido. El historial queda con un merge commit, y a cambio la resolución es
revisable en un solo diff.

Caso real (agentesia-web, 03-ago): rama de 16 commits, `HeroSection.tsx` reescrito 5 veces
mientras `main` metía 3 PRs sobre él. El rebase pidió resolver en el commit 1/15; el merge lo
pidió una vez. Ver [[al-mergear-main-en-rama-vieja-el-lado-que-borra-es-tu-base-desfasada]] ·
[[rama-nueva-desde-un-main-local-sin-fetch-revierte-trabajo-ajeno]]
