---
title: rama nueva desde un main local sin fetch revierte trabajo ajeno
date: 2026-08-01
source: claude-code-session
tags: [git, worktree, equipo]
---
`git worktree add -b feat/x ../wt main` usa el **main local**, no `origin/main`. Si
llevas días sin traer, la rama nace vieja y todo lo que edites encima pisa el trabajo
que otros ya mergearon.

Caso real (agentesia-web, 01-ago): el worktree salió de un main 4 commits por detrás.
Uno de esos commits (#91) había **centralizado las cifras del hero en una constante
`PROOF`** precisamente para que el mismo dato no apareciera con valores distintos según
la página. En la rama nueva se reescribieron esas stats a mano y con una cifra sin
respaldo — deshaciendo el arreglo sin enterarse. Otro commit (#89) había sacado la
animación fuera del `h1`, y la rama seguía trabajando sobre la versión con el efecto
dentro.

Fix: `git fetch && git worktree add -b <rama> <ruta> origin/main`. Y antes de tocar un
componente compartido, `git log main..origin/main -- <fichero>` para ver quién ha
pasado por ahí. Ver [[antes-de-arrancar-un-fix-mirar-el-log-del-area]]

Desenlace (03-ago): las dos regresiones se cazaron al integrar, y no leyendo el diff sino con la
**suite que `main` traía de nuevas** — los mismos PRs que la rama pisaba habían dejado un test de
integridad del heading y otro de prueba social. Un arreglo con test se defiende solo del trabajo
paralelo; sin test se pierde en el siguiente merge sin que nadie lo note. Ver
[[los-tests-rojos-que-hereda-un-merge-se-clasifican-uno-a-uno]] ·
[[rama-que-reescribe-el-mismo-fichero-varias-veces-se-integra-con-merge]]
