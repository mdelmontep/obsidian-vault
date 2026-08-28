---
title: el parche de un agente en worktree borra lo que no estaba commiteado si lo copias
date: 2026-08-28
source: agentesia-crm
tags: [subagentes, worktrees, integracion, git]
---

Un worktree nace del **último commit**, no del árbol sucio. Si coordinas N agentes mientras
integras a mano en `main` sin commitear, cada agente trabaja sobre una foto vieja y su parche
**revierte en silencio** lo que integraste después de esa foto.

- Se cobró dos veces el 28-ago: un agente devolvió un catálogo TS sin el registro que otro
  agente había añadido dos horas antes —y del que dependía un gate—, y otro devolvió un
  `salud.ts` sin las 198 líneas que main ya tenía.
- **Copiar el fichero del worktree es el error; fusionar el hunk es lo correcto.** Y `git apply
  -3` no ayuda: falla con «does not match index» en cuanto el fichero está modificado en el
  árbol. Extrae el hunk del `.patch` y aplícalo suelto.
- El mismo choque en SQL: dos migraciones paralelas, una borra una firma con `drop function` y
  la otra le pone un `comment on` — la segunda revienta el replay entero. Ordénalas y haz que
  el comentario de la última diga **las dos cosas**: el último `comment on` gana y el anterior
  no queda en ninguna parte.

Antídoto barato: commitea antes de lanzar la tanda, o asume que integrar es fusionar.

Ver [[cherry-pick-4-worktrees-agentes-paralelos]] ·
[[stash-es-compartido-entre-worktrees-y-rompe-sesiones-paralelas]] · [[audits-cross-pr-vs-per-pr]]
