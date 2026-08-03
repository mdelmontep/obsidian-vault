---
title: un trinquete que cuenta por regex también cuenta lo que hay en los comentarios
date: 2026-08-03
source: claude-code-session
tags: [tooling, ratchets, linters, hooks]
---

Un trinquete casero (contar `style={{`, `<button`, hex crudos y compararlo con un
baseline) cuenta ocurrencias en el **texto**, no en el AST. Consecuencia práctica y
absurda: **explicar por escrito que evitaste el patrón rompe el commit**.

Caso real: un comentario que decía «se resuelve con selector de atributo porque un
`style={{ paddingLeft }}` aquí rompería el trinquete» hizo subir el contador de ese
fichero de 0 a 1 y abortó el commit. El código estaba bien; lo que sobraba era la cita.

Dos lecturas, y las dos importan:
- Al escribir el comentario, no cites el patrón prohibido literalmente. Descríbelo.
- Si el trinquete es tuyo, quítale comentarios antes de contar. Y si ya lo hace, revisa
  el caso: suele fallar cuando la línea no **empieza** por `//` (comentario indentado, o
  comentario de bloque en JSX).

El fallo es benigno (bloquea, no deja pasar) pero desconcierta, porque el diff que ves no
tiene nada malo. Ver [[reglas-duras-en-prosa-acaban-en-hook]].
