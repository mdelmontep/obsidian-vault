---
title: un cierre de tanda compartido condena al rojo a la corrida que no comparte su precondición
date: 2026-08-19
source: facturaia
tags: [testing, playwright, guards, harness]
---

El `globalTeardown` de Playwright es **uno para toda la config**, no por proyecto. El de esta suite exige que el servidor contra el que se midió siga vivo (candado bueno: sin él, un `next dev` muerto a mitad da errores de conexión indistinguibles de un bug del producto). Pero el proyecto que **no usa servidor** —la maqueta monta el componente con el CSS del repo— no puede satisfacer esa poscondición: `e2e:layout` salía con `ec=1` con sus 18 casos en VERDE. Un gate que no puede salir verde enseña a ignorar el rojo; el daño no es el falso negativo, es entrenar a saltarse el semáforo.

La exención se decide por **cómo se invocó la tanda**, no por lo que pasó dentro: una variable explícita, o que TODOS los `--project=` pedidos lleven la marca en la config. Dos detalles sostienen el equilibrio:
- La tanda **mixta** (con servidor y sin) SÍ comprueba: el predicado es «alguno lo necesita», no «alguno no». Ese es el caso que discrimina y el que hay que escribir como test.
- Un `--project` que no existe (mal escrito, retirado) cuenta como que **sí** lo necesita: el lado seguro es comprobar.

El test del predicado no puede vivir junto al teardown si Vitest excluye `tests/e2e/**` — ahí no correría nunca. Y un caso debe aseverar contra el `playwright.config.ts` REAL: si no, pasa con una config de juguete mientras el fichero de verdad pierde la marca en un merge.

**Y el mismo arnés tenía el defecto gemelo, más caro (#1974): comprobaba que ALGO respondiera en `baseURL`, no que respondiera TU checkout.** Con `.env.test` fijando un puerto y varios worktrees vivos, toda la suite medía el código de otra rama en silencio, y una tanda «sin servidor» salía VERDE informando de «servidor vivo» porque había uno: el de otro. Lo que anotaba el setup (baseURL, puerto, pids) no incluía nada del checkout, así que era indetectable por dentro. Fix: comparar el `cwd` del proceso que escucha con la raíz del árbol y plantarse, con escape explícito. Dos gotchas al probarlo: un test con el pid 1 **no discrimina** (macOS no deja leer el `cwd` de `launchd`, así que la función responde «no afirmo nada» y sale verde por el motivo equivocado), y `resolve()` no canoniza symlinks —en macOS `/tmp` es `/private/tmp`—, así que hay que comparar con `realpath` o un dev server lanzado por un symlink da un falso «servidor ajeno».

Ver [[tanda-e2e-sin-comprobar-el-servidor-vivo-al-final-no-es-medicion]] · [[la-maqueta-se-mide-con-el-motor-no-se-modela-sumando-anchos]] · [[facturaia]].
