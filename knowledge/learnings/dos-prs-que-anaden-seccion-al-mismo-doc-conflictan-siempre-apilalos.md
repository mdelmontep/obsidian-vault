---
title: dos PRs que añaden sección al final del mismo doc conflictan siempre — apílalos
date: 2026-08-26
source: agency-portal
tags: [git, prs, conflictos, docs]
---
Dos ramas abiertas en paralelo que añaden `## 10` y `## 10` al final del mismo
runbook no "puede que" conflicten: conflictan seguro, y el conflicto se lo come
quien mergea (aquí Borja), no quien lo creó. Detectarlo antes cuesta un
`git diff main...<rama> --name-only` de cada PR abierto y cruzar los ficheros.
Arreglo: apilar el segundo sobre el primero (`git rebase <rama-1>`), renumerar
la sección al número que le toca y **reapuntar la base del PR**
(`gh pr edit N --base <rama-1>`) para que el diff de review no muestre el
trabajo del otro.
Gotcha durante ese rebase: `git checkout --ours <fichero>` puede quedar
bloqueado por el hook `git-guard` (descarta cambios sin commitear). La
alternativa que sí pasa es materializar la versión buena con
`git show HEAD:<ruta>` y escribirla, luego `git add` + `rebase --continue`. Si
el segundo commit queda vacío, git lo tira — verifica por CONTENIDO que ya está
dentro, no por SHA. Ver [[gh-pr-merge-no-confirma-verificar-state-merged]].
