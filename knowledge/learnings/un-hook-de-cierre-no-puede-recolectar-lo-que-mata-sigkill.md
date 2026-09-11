---
title: un hook de cierre no puede recolectar nada, porque el peor caso no ejecuta código
date: 2026-09-11
source: claude-harness
tags: [hooks, claude-code, arnes, diseño]
---
Tentación al diseñar limpieza de estado residente (contenedores, navegadores headless, dev
servers, worktrees): un hook `SessionEnd` que reclame lo que esa sesión levantó.

No basta, y no es un hueco de documentación: es semántica del SO. Un proceso que recibe SIGKILL
**no ejecuta nada** — el kernel lo siega. El OOM killer de macOS (jetsam) mata así. Igual un
apagón o un `kill -9`. Y el caso en que más falta hace recoger es exactamente ése.

Reparto correcto, y el orden importa:
- `SessionEnd` → el cierre educado (`/exit`, Ctrl-D). Es la mitad barata.
- **Barrido por antigüedad** → el caso brutal. NO es un complemento, es lo obligatorio.

Casa natural del barrido: un proceso que ya corre a menudo por otro motivo (en este arnés, el
`reap_orphans` del semáforo). No hace falta demonio nuevo.

Corolario al probarlo: el caso que DEBE recoger es el de padre muerto, no el de padre vivo.

Y si el hook guarda un marcador, ojo con dónde: [[git-worktree-dotgit-es-fichero-basename-devuelve-la-rama]]. `--git-common-dir` si el marcador es POR SESIÓN; `--git-dir` si es POR ÁRBOL. No son intercambiables.
