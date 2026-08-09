---
title: probar hooks de git en el repo real puede dejarlo en core.bare y bloquear a los demás
date: 2026-08-09
source: claude-code-session
tags: [git, hooks, worktree, incidente]
---
Con dos sesiones sobre el mismo árbol, una probando hooks de git, el repositorio apareció con
`core.bare = true`: `git status` pasó a responder «this operation must be run in a work tree»
aunque los ficheros y el historial estaban intactos. Aparecieron además `src/rastreado.ts`,
`src/se-borra.ts` y un commit local «inicial» que borraba `.audit-baseline.json` y varios
hooks — nada llegó al remoto.

Arreglo: `git config core.bare false`. No se pierde nada; es sólo que git deja de ver el árbol.

Y el síntoma previo, más difícil de atribuir: `git commit` moría con **«error: Error building
trees»** porque el índice cambiaba durante los dos minutos que tarda un pre-commit pesado.

Dos reglas: los hooks se prueban en un repo desechable (`git init` en `/tmp`), y la segunda
sesión sobre un repo va en `git worktree`. Ver [[antes-de-tocar-un-ticket-mira-si-otra-sesion-ya-lo-esta-cerrando]].
