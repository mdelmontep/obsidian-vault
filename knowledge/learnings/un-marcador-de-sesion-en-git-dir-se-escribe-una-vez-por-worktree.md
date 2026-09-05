---
title: un marcador de «una vez por sesión» guardado en `--git-dir` se escribe una vez por WORKTREE
date: 2026-09-06
source: claude-code-session facturaia
tags: [git, worktree, hooks, harness, gotcha]
---
Un hook `Stop` avisaba «una vez por sesión» y avisaba de más. Causa: guardaba su marcador en
`$(git rev-parse --git-dir)`, que en un worktree es **privado de ese worktree**
(`.git/worktrees/<nombre>/`), no compartido. Con siete worktrees vivos, la misma sesión
escribía siete marcadores distintos y creía ser nueva siete veces.

- `--git-dir` → el directorio git **de este worktree**. Sirve para estado local (HEAD, index).
- `--git-common-dir` → el `.git` **compartido** por todos. Ahí va cualquier estado que deba ser
  único por repo: marcadores de sesión, cachés, semáforos, contadores.

Y devuelve **ruta relativa** cuando lo lanzas desde la raíz, así que hay que absolutizarla o el
marcador acaba en el cwd de quien invocó el hook:

```sh
gitcommon=$(git rev-parse --git-common-dir 2>/dev/null || echo "$root/.git")
case "$gitcommon" in /*) ;; *) gitcommon="$root/$gitcommon" ;; esac
```

Recordar además que en un worktree `.git` es un **fichero**, no un directorio: cualquier hook que
haga `test -d "$root/.git"` o escriba dentro lo falla en silencio.

Medido al revés, que es como se prueba un guard: mismo hook, misma sesión, segundo worktree →
`avisa=1` con el código viejo, `avisa=0` con el nuevo. Ver
[[una-suite-en-verde-no-prueba-el-camino-real]].
