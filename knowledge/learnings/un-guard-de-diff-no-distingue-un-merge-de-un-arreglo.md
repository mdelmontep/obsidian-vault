---
title: un guard que juzga el diff no distingue un merge de un arreglo, y bloquea el merge
date: 2026-08-23
source: claude-code-session facturaia
tags: [hooks, git, arnes, falso-positivo]
---
`mutate-guard` bloquea un commit que toca código y tests a la vez sin haber visto el rojo. Correcto
para un arreglo. Pero un **merge commit de `origin/main`** trae en su diff todo lo que entró en main
desde que salió la rama — decenas de ficheros de código y sus tests — y el hook lo lee como el patrón
que persigue. El 22-ago cortó la composición de un PR con main, y lo que listaba como «código sin
test» eran cambios **ya mergeados y ya verificados por mutación**.

Salida sin rodearlo: **`git rebase origin/main` en vez de `git merge`**. El rebase no crea un commit
nuevo con ese diff (reaplica los que ya pasaron el hook en su día) y **no dispara `pre-commit`**.
Resuelve el conflicto del fichero generado con `--continue`, que tampoco lo dispara.

Regla al escribir un guard sobre el diff: **preguntar antes por la forma del commit**, no solo por su
contenido. `git rev-parse -q --verify MERGE_HEAD` distingue un merge en curso; un rebase se detecta
por `REBASE_HEAD` o el directorio `rebase-merge`. Sin eso, el hook grava justo la operación que más
conviene hacer a menudo — recomponer con main —, y empuja al `--no-verify` que existe para evitar.

Ver [[el-hueco-esta-en-el-cableado-no-en-la-funcion-pura]] ·
[[guard-hooks-matchear-comando-sin-comillas-no-substring-cruda]] ·
[[hook-que-resuelve-git-en-el-cwd-de-la-sesion-juzga-el-repo-equivocado]]
