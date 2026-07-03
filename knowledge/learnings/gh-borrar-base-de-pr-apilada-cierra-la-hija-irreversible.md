---
title: gh — borrar la base de una PR apilada cierra la PR hija (irreversible); retargetear antes
date: 2026-07-04
source: claude-code-session
tags: [git, github, gh]
---
En un tren de PRs apiladas (cada base es la rama anterior), `gh pr merge --delete-branch` sobre una
PR **cierra la PR hija** si su base (rama) desaparece antes de que GitHub la retargetee — y una PR
cerrada con la base borrada **NO se puede reabrir** (hay que recrear la rama → PR nueva, se pierde el
número y el hilo de review).

Protocolo para trenes apilados:
- **Retargetear las PRs hijas a `main`** (o a la nueva base) ANTES de mergear/borrar la base.
- O mergear SIN `--delete-branch` y borrar las ramas al final, cuando todo está en `main`.

Caso real: tren AGH Ibérica — la #60 murió al borrarse su base y se recreó como #68 (mismo contenido).
Relacionado con la disciplina de imanes de conflicto en repos con varias sesiones en paralelo.
