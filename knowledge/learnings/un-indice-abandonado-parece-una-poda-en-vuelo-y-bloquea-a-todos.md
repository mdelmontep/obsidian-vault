---
title: un índice abandonado parece una poda ajena en vuelo y bloquea a todo el mundo
date: 2026-09-20
source: obsidian-vault
tags: [git, vault, sesiones-paralelas, trabajo-en-paralelo]
---

`git status` con cientos de rutas y decenas de borrados **staged** se lee como «otra sesión
tiene una poda a medias»: no se toca nada y se espera a que aterrice. En el vault eso costó
**cuatro cierres seguidos** sin actualizar hubs ni `top-of-mind`, con la espera heredada en
memoria como si fuera un hecho.

**No era una poda: era un índice de hace una semana que nadie volvió a mirar.** Lo que lo
delata, y ninguna de las tres cosas se ve en `git status`:

- Los ficheros «borrados» **siguen en disco** (`D ` staged + fichero presente = nadie los borró).
- El diff staged de un fichero **quita** líneas que `HEAD` ya tiene: el índice va *hacia atrás*.
- `git write-tree` y comparar ese árbol con los últimos commits da el día en que se congeló
  (aquí: 240 rutas de diferencia contra el del 13-sep, 316+ contra todos los posteriores).

Commitearlo habría borrado 104 learnings vivos. Fix, sin perder nada: `git commit-tree $(git
write-tree) -p HEAD` + `git update-ref refs/backup/<nombre>` para anclarlo, y después
**`git reset` a secas** — sincroniza índice y `HEAD` y **no toca el árbol de trabajo**
(verificado con el listado de ficheros antes y después). Quedaron 96 de las 596 líneas.

Corolario: el bloqueo se cobra dos veces, porque el crecimiento del trinquete de contexto se
atribuye a «la poda sin commitear» cuando en realidad ya estaba en `main`.
Ver [[un-script-que-mezcla-indice-y-head-se-contradice-con-un-rename-staged]] ·
[[claude-code-sesiones-paralelas-mismo-repo-colisiones-git]] ·
[[triaje-seguro-ramas-worktrees-sesiones-paralelas]]
