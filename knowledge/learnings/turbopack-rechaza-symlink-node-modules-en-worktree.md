---
title: turbopack rechaza node_modules symlinkeado en un worktree (tsc/vitest sí lo aceptan)
date: 2026-06-21
source: claude-code-session
tags: [nextjs, turbopack, worktree, git]
---

En un `git worktree` nuevo, enlazar deps con `ln -s …/repo/node_modules node_modules`
hace funcionar `tsc --noEmit` y `vitest`, pero **`next build` (Turbopack) aborta**:
`FATAL … Symlink [project]/node_modules is invalid, it points out of the filesystem root`.

El engaño es que tsc/vitest no tocan Turbopack, así que pasan verde con el symlink y
solo el build/dev lo destapa.

**Fix rápido** (2026-06-24): crea el worktree en el MISMO volumen que el repo y
`cp -al repo/node_modules node_modules` (hardlinks: instantáneo, 0 disco extra, Turbopack
OK). El symlink solo revienta si cruza filesystem root (`/private/tmp` ↔ `/Users`).
`npm install` real (~1-2 min + disco) solo si no puedes co-ubicar el worktree.

**Gotcha del propio fix** (2026-07-06): si el comando `cp -al` se corta a mitad
(timeout del shell, Ctrl-C) deja una copia PARCIAL sin error visible — el conteo
de entries en la raíz de `node_modules` puede coincidir a simple vista pero
falta algún paquete anidado (p. ej. `debug` dentro de `ioredis`), y el síntoma
solo aparece más tarde como `Module not found` al arrancar `next dev`. Verificar
con `ls node_modules | wc -l` origen vs copia antes de dar la copia por buena;
si no cuadra, `rm -rf` y repetir `cp -al` completo sin interrupciones.

**Gotcha del symlink con git (2026-07-07):** si usas el symlink (ok en proyectos sin
Turbopack, p. ej. backend Node), `git stash push -u` se lo lleva al stash (es untracked) →
tras un `checkout -b` el symlink puede no volver y `vitest`/`tsc` rompen con
`Cannot find package 'vitest'`. Recrear el symlink antes de correr tests (o mover cambios
entre ramas sin `-u`). Ver [[git-stash-sin-u-deja-untracked-y-hook-falla]].

**Contraejemplo del "mismo volumen" (2026-07-29):** worktree en `~/Projects/wt-x` con
symlink a `~/Projects/repo/node_modules` — mismo disco, mismo `/Users` — y Turbopack lo
rechaza igual con el mismo FATAL. Co-ubicar en el volumen NO basta. Si el worktree cuelga
fuera del repo, `cp -al`; el symlink solo vale anidado (abajo).

**Excepción confirmada (2026-07-29, Next 16.2.11):** con el worktree ANIDADO dentro del
propio repo (`.claude/worktrees/<x>`), el symlink de `node_modules` (+ `.env.local`) SÍ deja
pasar `next build`: apunta dentro del filesystem root, que es lo único que Turbopack exige.
Gate completo verde sin `npm install` ni `cp -al`. Único ruido: Next avisa de "multiple
lockfiles" y elige el del repo padre. La regla real no es "symlink no", es "el symlink no
puede salir del root".

**Por qué duele tanto (2026-07-29):** el gate pre-push muere en `build`, o sea DESPUÉS de que
lint, typecheck y tests hayan pasado en verde con el symlink puesto. El error habla de symlinks y
filesystem root, pero llega en el momento en que uno espera un error de código, así que se lee
como regresión propia. Si el worktree va a pasar el gate completo, resuelve `node_modules` de
verdad (anidado + symlink, `cp -al` o `cp -Rc`) antes de escribir la primera línea.

**También revienta `next dev`, no solo el build (2026-08-03):** mismo FATAL al levantar el
servidor, así que el symlink tampoco vale si vas a mirar algo en el navegador. Y ojo al dejarlo
puesto: un `npm install` lanzado desde el worktree escribe en el `node_modules` del repo padre.
Coste real del `npm ci` en el worktree: ~2 min con caché caliente y ~1 GB. Copia también
`.env.local`, que no se hereda y el build lo necesita.

**Reincidido dos veces más (13-ago y 14-ago), y esta nota no lo evitó** porque nadie la lee al
CREAR el worktree: se lee cuando el build ya ha fallado, media hora después. Conclusión práctica:
en un worktree que vaya a pasar el gate, **copiar siempre** — `cp -Rl` (hardlinks, instantáneo)
si comparte volumen, `cp -R` (~30 s en APFS) o `npm ci` (~2 min, ~1 GB) si no. El symlink solo se
justifica en un worktree anidado dentro del repo, o en proyectos sin Turbopack. Es candidato claro
a hook en el comando que crea worktrees, que es el único momento en que la regla se aplicaría sola.
(Fusionado aquí el duplicado `turbopack-build-rechaza-node-modules-symlink-en-worktree`, 14-ago.)

**Tercera y cuarta reincidencia (17-ago), las dos en la MISMA sesión** y con esta nota ya escrita: dos
worktrees enlazados con `ln -s`, lint/typecheck/vitest/suite completa en verde en ambos, y los dos
parados por el pre-push en `build`. Confirma el diagnóstico de arriba: la nota no falla por contenido,
falla por MOMENTO — se consulta cuando el build ya reventó, nunca al crear el worktree. Con cuatro
reincidencias medidas, el hook al crear worktrees deja de ser «candidato claro» y pasa a ser la única
salida: lo que se arregla leyendo, no se arregla.

**Quinta reincidencia (30-ago) con firma DISTINTA: `node_modules` VACÍO, ni symlink ni copia.**
En un worktree ANIDADO (`.claude/worktrees/<x>`), la resolución de Node sube por el árbol
hasta el `node_modules` del repo padre, así que **lint, vitest y `tsc` pasan en verde sin
tener nada instalado**. Solo revienta el build, y con un mensaje que no menciona worktrees
ni symlinks: «We couldn't find the Next.js package (next/package.json)». Se lee como
instalación corrupta del repo padre. Fix: `npm ci` en el worktree, lo primero, antes de la
primera línea de código — mismo consejo de siempre, un síntoma nuevo por el que llegar tarde.

Ver [[triaje-seguro-ramas-worktrees-sesiones-paralelas]] · [[worktree-facturaia-build-supabase]] ·
[[worktree-qa-next-standalone-symlink-node-modules]] · [[worktree-monorepo-symlink-node-modules-anidado]].

**Sexta reincidencia (3-sep), en un worktree anidado y con la memoria del agente avisando:** `ln -s`
al `node_modules` del padre, suite verde, y el pre-push muerto en `build` con el mismo FATAL. Fix
`rsync -a` (copia real). La excepción del worktree anidado de julio ya no se cumple: no fiarse de ella. Y el gate de ese mismo día necesitó además [[tsc-de-un-repo-grande-desborda-el-heap-por-defecto-de-node-aunque-corra-solo]].
