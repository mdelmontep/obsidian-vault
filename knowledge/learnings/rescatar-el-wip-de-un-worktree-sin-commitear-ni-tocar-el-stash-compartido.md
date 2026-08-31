---
title: rescatar el WIP de un worktree sin commitear ni tocar el stash compartido
date: 2026-08-31
source: claude-code-session
tags: [git, worktrees, housekeeping, agentes-paralelos]
---
Al retirar worktrees viejos hay dos hechos que cambian el cálculo del riesgo:

1. **`git worktree remove` NO borra la rama.** Los commits siguen vivos y alcanzables por
   `git log <rama>`. Lo único que se pierde es lo **no commiteado**. Así que de 39 worktrees,
   los 80 % con commits propios se retiran sin pensar; solo hay que mirar los sucios.
2. Para salvar esos sucios, **ni commitear ni `git stash`**. Commitear trabajo «a medias»
   choca con los hooks del repo y salir de ahí pide `--no-verify`, que no se toca. Y el stash
   es COMPARTIDO entre worktrees ([[stash-es-compartido-entre-worktrees-y-rompe-sesiones-paralelas]]).

La salida son las dos mitades de `stash` por separado: `stash create` fabrica el commit y no lo
apila en ningún sitio; `update-ref` lo hace permanente y alcanzable con nombre propio.

```sh
git -C "$wt" add -A                 # así los untracked entran también
sha=$(git -C "$wt" stash create "wip $n")
[ -n "$sha" ] && git update-ref "refs/wip/<proyecto>/$n" "$sha"
git worktree remove --force "$wt"   # recuperar: git stash apply refs/wip/<proyecto>/$n
```

Y antes de creer que un worktree tiene trabajo vivo: **«sucio» no es «adelantado»**. Doce de
agentesia-crm salían modificados y su contenido era el VIEJO — `main` los había superado.
Se mide fichero a fichero: `git show origin/main:$f | diff -q - "$wt/$f"`.
Ver [[triaje-seguro-ramas-worktrees-sesiones-paralelas]].
