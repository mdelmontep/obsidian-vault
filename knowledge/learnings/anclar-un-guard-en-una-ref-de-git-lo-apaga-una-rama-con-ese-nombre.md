---
title: anclar un guard en `rev-parse MERGE_HEAD` lo apaga para siempre una rama con ese nombre
date: 2026-08-23
source: claude-code-session facturaia
tags: [hooks, git, arnes, seguridad]
---
Al eximir los merges en `mutate-guard` ([[un-guard-de-diff-no-distingue-un-merge-de-un-arreglo]]), el
ancla natural parece `git rev-parse -q --verify 'MERGE_HEAD^{commit}'`. **No sirve**: `rev-parse`
resuelve por el ORDEN DE REFS de git — primero `$GITDIR/MERGE_HEAD`, y si no, `refs/MERGE_HEAD`,
`refs/tags/…`, `refs/heads/…`. Así que `git branch MERGE_HEAD` (o `git tag CHERRY_PICK_HEAD HEAD`, o
`git update-ref refs/REVERT_HEAD HEAD`) da la excepción por buena. Y git **no borra** esas refs al
commitear: el guard queda muerto en ese repo **para siempre**, con `git status` diciendo «On branch
main». Un comando normal, cero rastro.

Ancla en el **FICHERO** de estado del gitdir y en su contenido: sha crudo (40/64 hex, porque
`cat-file -t` acepta `HEAD~1` y nombres de rama) **de tipo `commit`**, más el estado que git escribe al
lado (`MERGE_MODE`+`MERGE_MSG` para merge; `MERGE_MSG` para cherry-pick y revert; el directorio para
rebase). Sube el precio de 1 comando a reconstruir el estado entero. `sequencer/` NO vale: un
cherry-pick de un solo commit no lo crea.

Y no eximas el commit: **descuenta del stage** lo que la operación explica (`diff HEAD $sha` ∪
`diff $sha^ $sha`) y aplica la regla al resto. Eximir abre el caso mixto — un merge real con tu arreglo
y tu test colados dentro.
