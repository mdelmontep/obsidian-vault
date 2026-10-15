---
title: gate-remoto --help lanza un gate, y un fichero sin trackear lo bloquea
date: 2026-10-15
source: facturaia
tags: [gate, vm, harness]
---
Dos trampas de `~/bin/gate-remoto` (el que corre etapas del gate en la VM):
- **`--help` no imprime ayuda**: lo toma como orden y lanza un gate entero. Para ver el uso, lee
  la cabecera del script.
- **Exige el árbol limpio, también sin `??`**: una `.scratch/` sin trackear dentro del worktree
  hace que salga con `ec=2`. Borra la carpeta, o ponla fuera del worktree, antes de lanzarlo.
  Los scripts de Workflow tienen que vivir en el proyecto, así que hay que borrarlos al acabar.

Y si la VM se queda sin disco (le pasó al 100 % el 14-oct), tumba los pushes que pasan por ella.
El síntoma parece de red.

Ver [[la-cola-del-gate-miente-en-dos-direcciones]].
