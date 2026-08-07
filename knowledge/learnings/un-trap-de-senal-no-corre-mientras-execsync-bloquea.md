---
title: un trap de SIGINT no corre mientras execSync bloquea el event loop
date: 2026-08-07
source: claude-code-session
tags: [node, procesos, limpieza, herramientas, verificacion]
---
`process.on("SIGINT"|"SIGTERM")` **no se ejecuta** mientras un `execSync`/`spawnSync` tiene bloqueado
el event loop. Si el trabajo peligroso ocurre precisamente durante esa llamada síncrona —el caso
típico: un proceso que modifica ficheros y lanza tests con `execSync`— el trap es decorativo: solo
corre cuando ya no hace falta.

AGH 7-ago: barrido de mutación matado con un mutante escrito → `git status` seguía enseñando código de
producción alterado, a un `git commit -a` de colarse en una PR. El trap estaba puesto **y con tests en
verde**; lo tumbó matarlo de verdad, con un mutante en vuelo.

- Para estado que hay que poder recuperar: **diario en disco**, no manejadores. Escribir el original
  ANTES de tocar el fichero y restituirlo en el arranque siguiente. Aguanta `SIGKILL`.
- La restauración va **antes** de la comprobación de árbol limpio; si no, lo que quedó a medias impide
  arrancar y hay que limpiarlo a mano.
- Ojo al sitio del diario: en un **worktree `.git` es un FICHERO**, así que `<raíz>/.git/x` da
  `ENOTDIR` — usar `git rev-parse --absolute-git-dir`. Ver
  [[git-worktree-dotgit-es-fichero-basename-devuelve-la-rama]].
- Y `execSync` sin `timeout` deja el proceso colgado indefinidamente **con el fuente mutado**, sin
  error ni salida: parece que sigue trabajando.

Relacionado: [[barrer-el-diff-en-vez-de-mutar-a-mano]]
