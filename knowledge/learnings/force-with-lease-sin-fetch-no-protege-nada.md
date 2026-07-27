---
title: "--force-with-lease sin fetch previo no protege nada"
date: 2026-07-27
source: incidente TuFacturaIA — main rebobinada 40+ commits
tags: [git, incidentes, harness]
---

`--force-with-lease` NO compara contra el remoto: compara contra tu **referencia local**
`refs/remotes/origin/<rama>`. Si llevas horas sin `git fetch`, esa referencia está congelada en el
pasado y el lease da permiso alegremente para rebobinar todo lo que haya entrado desde entonces.

Caso real (2026-07-27): un `git push --force-with-lease` desde un checkout de `main` parado en
`22bf05ec` mientras `origin/main` iba por `cdf41473` → `+ cdf41473...22bf05ec main -> main (forced
update)`. Se llevó por delante 40+ commits de medio día: la tanda fiscal entera, el paso de
`middleware` a `proxy` y una fase completa ya mergeada, con sus migraciones **ya aplicadas en la BD de
producción**. Un deploy desde `main` en ese momento habría sido un rollback contra una BD migrada.

Reglas:

- El lease solo vale con un `git fetch` **inmediatamente antes**, en la misma línea:
  `git fetch origin && git push --force-with-lease origin …`.
- Mejor aún, lease con valor explícito: `--force-with-lease=main:<sha-que-esperas>`. Así no depende de
  cuándo fue tu último fetch.
- Nunca lanzar un push desde el checkout principal cuando el trabajo vive en un worktree: es
  justamente el checkout que nadie actualiza.

Lo que salvó la recuperación fue que la rama rebasada seguía intacta en su worktree, así que se pudo
reconstruir `cdf41473 + squash(rama)` y comparar árboles (`rev-parse HEAD^{tree}`) antes de volver a
empujar. El árbol, no el log, es lo que demuestra que no falta nada.

Ver [[git-head-compartido-entre-sesiones-paralelas-sin-worktree]]
