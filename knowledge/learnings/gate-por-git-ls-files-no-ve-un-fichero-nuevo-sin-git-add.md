---
title: un gate que enumera ficheros con git ls-files no ve uno nuevo hasta darle git add
date: 2026-08-06
source: claude-code-session
tags: [gates, git, ci, static-analysis]
---

Patrón común en gates de análisis estático propio (grep + identidad, no AST): enumerar el árbol con
`git ls-files` porque es rápido y respeta `.gitignore`. Pero `git ls-files` solo lista lo TRACKEADO —
un fichero recién creado y sin `git add` no aparece, así que un gate que debería fallar contra él sale
en verde por ausencia, no por corrección.

Caza real (TuCRMIA, 6-ago): un gate nuevo (`custom-fields-check.mjs`) decía "ningún fichero fuera del
módulo toca X" y pasaba en verde con un fichero nuevo que SÍ lo tocaba, simplemente porque aún no
estaba en el índice de git. `git add` primero y volver a correr el gate reveló el hallazgo real.

Antes de confiar en el verde de un gate nuevo (o de un cambio a uno existente) que enumera con
`git ls-files`: `git add` los ficheros nuevos del cambio que se está probando, y correr el gate DESPUÉS.
Sin eso, el "verde" solo demuestra que el gate corre, no que ve el árbol de verdad.
