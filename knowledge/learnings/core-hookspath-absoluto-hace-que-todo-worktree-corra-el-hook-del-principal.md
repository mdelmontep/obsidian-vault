---
title: core.hooksPath absoluto hace que TODO worktree corra el hook del checkout principal
date: 2026-09-08
source: facturaia
tags: [git, worktrees, hooks, gates, medicion]
---
`core.hooksPath` vive en `.git/config`, **compartido por todos los worktrees y fuera
del control de versiones**. Su forma decide qué hook corre, y la diferencia no está
documentada en ningún sitio obvio:

- `.githooks` (RELATIVO) → cada worktree corre **el suyo**.
- `/ruta/absoluta/.githooks` → **todos** corren el del árbol apuntado.

Medido en un repo de pruebas con un `pre-commit` distinto en cada árbol, no supuesto.
Basta un `git config core.hooksPath "$PWD/.githooks"` —o cualquier herramienta que
normalice a absoluto— para reabrirlo en silencio.

El daño no se ve porque **el fallo se disfraza de buena noticia**: si el árbol
apuntado va por detrás, tu push corre un gate con menos etapas y el log sale MÁS
CORTO. El 8-sep-2026 en facturaia fueron 175 commits de atraso y cuatro etapas
ausentes (integración, maqueta, pre-vuelo de base, núcleo-vs-dominio).

Dos arreglos, y hacen falta los dos: un caso en la **suite** que exija el valor
relativo (ver [[el-detector-de-un-instrumento-roto-vive-en-la-capa-que-el-roto-sigue-ejecutando]]),
y que el hook imprima al final **qué hook corrió y qué etapas ejecutó** — acumuladas
por quien las ejecuta, porque varias son condicionales y una lista escrita a mano
vuelve a ser una promesa. Ver [[worktree-facturaia-build-supabase]].
