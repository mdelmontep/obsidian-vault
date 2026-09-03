---
title: arreglar el hook y no la instrucción que lo ejecuta deja el paso apuntando a la ruta vieja
date: 2026-09-03
source: facturaia
tags: [harness, hooks, skills, worktree, git]
---
El hook `fia-cierre-reminder.sh` se arregló el 2-sep para leer el marcador en `--git-dir`. La skill
`/fia-cierre`, que es quien lo ESCRIBE, se quedó en `$(git rev-parse --show-toplevel)/.git/…`. En un
worktree ese `.git` es un **fichero**: el `touch` moría con `Not a directory`, el marcador no se creaba
nunca y el recordatorio salía en cada turno de cada sesión de worktree — justo lo que enseña a ignorarlo.

Dos cosas lo hacen difícil de ver: **en el checkout principal las dos rutas coinciden por accidente**,
así que el fallo solo existe donde ya no miras; y yo leí el `Not a directory` como «comportamiento de
worktree, por diseño» en vez de como avería — el tripwire literal del CLAUDE.md: si tu explicación es
«es por diseño», valida el RESULTADO.

Patrón: un arreglo que toca el lector y no el escritor no está terminado. Al arreglar un contrato de dos
lados, **grep del símbolo por todo el árbol** (aquí `fia-cierre-ran`), no solo del fichero que falla. Y
el candado es un test espejo que compare lo que la instrucción DICTA con lo que el hook LEE
(`scripts/__tests__/fia-cierre-reminder.test.ts`), no cada lado por su cuenta.
Ver [[verificar-que-un-test-tiene-dientes-con-una-mutacion]] y [[el-fix-que-propone-una-auditoria-puede-no-cerrar-el-agujero-que-describe]].
