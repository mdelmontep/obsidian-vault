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

**Variante sin `core.hooksPath`: los hooks de Claude Code** (`Stop`, `PreToolUse`…) salen de
`$CLAUDE_PROJECT_DIR/.claude/hooks/`, que es **siempre el checkout principal**, corras donde
corras. Si ese árbol va atrasado —y `git-guard` impide ponerlo al día mientras haya worktrees
vivos, así que el atraso es permanente— todas tus sesiones ejecutan arneses viejos.

Y el daño peor no es ejecutar el viejo, es **diagnosticar sobre él**: el 9-sep-2026 leí
`.claude/hooks/fia-cierre-reminder.sh` desde el principal (211 commits por detrás), le
diagnostiqué un bug real y propuse un arreglo. Estaba arreglado en `origin/main` desde hacía
semanas, y mi arreglo de una línea habría **reintroducido** el fallo que aquel PR cerró.
Antes de afirmar qué dice un fichero del arnés: `git show origin/main:<ruta>`.
