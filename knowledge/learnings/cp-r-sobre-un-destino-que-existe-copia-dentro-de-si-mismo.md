---
title: cp -R sobre un destino que existe copia dentro de sí mismo
date: 2026-08-16
source: claude-code-session
tags: [shell, node, worktrees, debug, falsos-positivos]
---

Truco habitual para no reinstalar en cada worktree: `cp -Rc node_modules ~/wt-X/node_modules`.
El `git worktree add` falló, el `cd ~/wt-X` encadenado con **`;`** falló con él, y el `cp`
siguiente corrió **en la raíz del repo** — donde el destino ya existía, así que copió el
directorio **dentro de sí mismo**: `node_modules/node_modules/react`.

Síntoma: **16 tests de React en rojo** con `TypeError: Cannot read properties of null
(reading 'useMemo')` — dos copias de React, hooks a `null`. El mensaje **no se parece en nada
a su causa**: sugiere React roto o versiones incompatibles.

Y era peor que un rojo cualquiera porque **confirmaba la hipótesis que yo perseguía**: cada
rama había pasado sola y buscaba un acoplamiento que solo apareciera al combinarlas.

Fix y regla:
- encadenar con **`&&`**, nunca `;`, cuando lo de después depende del `cd`;
- ante un rojo que **confirma** tu hipótesis, **lee la ruta del stack** antes de creértelo:
  un `node_modules/` repetido, un `dist/` ausente o un fichero fuera de `.dockerignore` dan
  mensajes de fallo real ([[un-rojo-ajeno-con-cara-de-real-dump-rdb-y-web-dist]]);
- antes de arreglar, **mide el alcance**: barrer los 8 worktrees dijo que solo 2 estaban
  contaminados y ninguno de los que produjeron las mediciones que decidieron el merge.
