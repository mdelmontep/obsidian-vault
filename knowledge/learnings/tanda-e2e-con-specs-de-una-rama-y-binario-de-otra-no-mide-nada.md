---
title: una tanda E2E con los specs de una rama y el binario de otra no mide nada
date: 2026-08-01
source: claude-code-session
tags: [e2e, testing, playwright, git, worktree]
---
Lancé la suite desde el repo raíz (en `main`, con el spec viejo) contra un servidor construido con
el código de la rama: **6 fallos**. Repetida desde el worktree de la rama, con sus specs y su
binario: **1**. Los otros 5 eran la mezcla de versiones, y uno de ellos (`modulo-config-autosave`)
me tuvo un rato buscando una regresión que no existía.

Playwright coge los specs del `cwd`; el servidor sirve el `.next` de donde se construyó. Con
worktrees esos dos sitios se separan sin avisar y el marcador sigue saliendo, con pinta de válido.

Reglas:
- Correr la suite SIEMPRE desde el mismo checkout que construyó el servidor. Comprobarlo, no
  suponerlo: `git -C <dir> log -1 -- <ruta-del-spec>` en los dos lados.
- Un rojo se clasifica construyendo `origin/main` **en el mismo worktree**, con el mismo servidor y
  los mismos datos. Si falla igual, es preexistente; ahí se acaba la discusión.
- Contención ≠ preexistente ≠ regresión: lo aislado descarta contención, lo de `main` descarta
  regresión.

Ver [[auditar-sobre-origin-main-worktree-no-cwd-stale]] ·
[[un-checker-que-se-pone-rojo-por-la-razon-equivocada-es-peor-que-no-tenerlo]]
